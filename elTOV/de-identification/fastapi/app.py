import uvicorn
from fastapi import FastAPI , Request
from face import FaceBlur
import numpy as np
import cv2
import asyncio
import datetime as dt
from pytz import timezone
import os
import shutil


class App:
    def __init__(self):        
        self.app = FastAPI()
        self.blur_model = FaceBlur()
        self.data_retention_time = 30
        self.min_free_hdd_capacity = 10
        self.cnt = 0
        
        
    async def serve(self):
        
        @self.app.post('/stream')
        async def stream_video(req:Request):
            writer = self.get_video_writer(width=int(req.headers.get('width')),hegith=int(req.headers.get('height')))
            cnt = 0
            async for data in req.stream():
                cnt += 1
                if len(data) > 0:
                    image = np.frombuffer(data, dtype=np.uint8)
                    frame = cv2.imdecode(image, cv2.IMREAD_COLOR)
                    if frame is not None:
                        frame= cv2.resize(frame,(408,612))
                        writer.write(frame)
            writer.release()
            return True
        
        
        @self.app.post("/save-video")
        async def save_image(request: Request):
            res = await request.body()
            image = np.frombuffer(res, dtype=np.uint8)
            frame = cv2.imdecode(image, cv2.IMREAD_COLOR)
            if frame is not None:
                frame = self.blur_model.pipe_blur(frame)
                if frame is not None:
                    file_name = self.get_log_path()
                    cv2.imwrite(file_name, frame)
            return True
        config = uvicorn.Config(self.app,host="0.0.0.0", port=5000,reload=True)
        server = uvicorn.Server(config)
        await server.serve()
    
    def get_log_path(self, ext = 'jpg'):
            time_now = dt.datetime.now(timezone('Asia/Seoul'))
            storage = os.statvfs("/")
            storage_total = storage.f_blocks * storage.f_frsize
            storage_free = storage.f_bavail * storage.f_frsize
            free_space_ratio = storage_free / (storage_total+0.00000001) * 100

            duration = dt.timedelta(days=self.data_retention_time)
            time_prev = time_now - duration
            prev_dir = "./image_log/{}/{}/{}".format(time_prev.year, time_prev.month, time_prev.day)
            
            if os.path.exists(prev_dir):
                shutil.rmtree(prev_dir)

            if free_space_ratio > self.min_free_hdd_capacity:
                cnt = self.cnt
                print('Free disk space : {} %'.format(free_space_ratio))
                out_dir = "./image_log/{}/{}/{}".format(time_now.year, time_now.month, time_now.day)
                out_fname = "{}_{}_{}_{}.{}".format(time_now.hour, time_now.minute, time_now.second,cnt,ext)
                os.makedirs(out_dir, exist_ok=True)
                path = os.path.join(out_dir,out_fname)
                while os.path.exists(path) != False:
                    cnt += 1
                    out_fname = "{}_{}_{}_{}.{}".format(time_now.hour, time_now.minute, time_now.second,cnt,ext)
                    path = os.path.join(out_dir,out_fname)
                self.cnt = cnt
                    
                
                
                return path
    def get_video_writer(self,width: int = 1280, hegith:int = 720):
        return cv2.VideoWriter('./video.mp4',cv2.VideoWriter.fourcc(*'DIVX'),20,(408,612))
        


async def start():
    app = App()
    await app.serve()

if __name__ == "__main__":
    asyncio.run(start())
            