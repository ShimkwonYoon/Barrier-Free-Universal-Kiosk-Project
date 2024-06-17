"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const node_webcam_1 = __importDefault(require("node-webcam"));
// import Webcam from "node-webcam/src/Webcam";
const os_1 = __importDefault(require("os"));
const defaultOptions = {
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
    output: "jpeg",
    //Which camera to use
    //Use Webcam.list() for results
    //false for default device
    device: false,
    // [location, buffer, base64]
    // Webcam.CallbackReturnTypes
    callbackReturn: "location",
    //Logging
    verbose: false,
    platform: os_1.default.platform(),
};
class NodeCameraController {
    constructor(opts = defaultOptions) {
        this.Webcam = node_webcam_1.default.create(Object.assign({}, (opts || defaultOptions)));
    }
    getCameras() {
        return __awaiter(this, void 0, void 0, function* () {
            return new Promise((resolve) => {
                this.Webcam.list(function (list) {
                    resolve(list.map((cam) => cam.replace("=> ", "")));
                });
            });
        });
    }
}
exports.default = NodeCameraController;
