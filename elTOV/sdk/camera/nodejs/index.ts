import NodeWebcam, {
  ImageSnapWebcam,
  WebcamOptions,
  WindowsWebcam,
} from "node-webcam";
// import Webcam from "node-webcam/src/Webcam";
import OS from "os";
type Platform = "linux" | "fswebcam" | "win32" | "win64" | "darwin";
type Options = WebcamOptions & {
  platform: "linux" | "fswebcam" | "win32" | "win64" | "darwin";
};
const defaultOptions: Options = {
  //Picture related

  width: 1280,

  height: 720,

  quality: 100,

  // Number of frames to capture
  // More the frames, longer it takes to capture
  // Use higher framerate for quality. Ex: 60

  frames: 60,

  //Delay in seconds to take shot
  //if the platform supports miliseconds
  //use a float (0.1)
  //Currently only on windows

  delay: 0,

  //Save shots in memory

  saveShots: true,

  // [jpeg, png] support varies
  // Webcam.OutputTypes

  output: "jpeg" as const,

  //Which camera to use
  //Use Webcam.list() for results
  //false for default device

  device: false,

  // [location, buffer, base64]
  // Webcam.CallbackReturnTypes

  callbackReturn: "location" as const,

  //Logging

  verbose: false,
  platform: OS.platform() as Platform,
};

export default class NodeCameraController {
  private readonly Webcam: ImageSnapWebcam | WindowsWebcam;
  constructor(opts: Options = defaultOptions) {
    this.Webcam = NodeWebcam.create({ ...(opts || defaultOptions) });
  }

  async getCameras(): Promise<string[]> {
    return new Promise((resolve) => {
      this.Webcam.list(function (list: string[]) {
        resolve(list.map((cam) => cam.replace("=> ", "")));
      });
    });
  }
}
