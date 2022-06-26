import 'dart:html';

import 'package:camera/camera.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
// import 'package:flutter/painting.dart';
import 'package:flutter/services.dart';
import 'package:google_ml_kit/google_ml_kit.dart';
// import 'package:google_mlkit_commons/google_mlkit_commons.dart';
// import 'package:google_mlkit_text_recognition/google_mlkit_text_recognition.dart';
import '../logger.dart';
// import '../main.dart';

class OcrTabView extends StatefulWidget {
  const OcrTabView({Key? key}) : super(key: key);
  @override
  State<OcrTabView> createState() => OcrTabViewState();
}

class OcrTabViewState extends State<OcrTabView> {
  // Create the CameraController
  late CameraController _cameraController;
  Future<void>? _initializeControllerFuture;
  List<CameraDescription> cameras = [];

  // Initializing the TextDetector
  final TextRecognizer textDetector =
      TextRecognizer(script: TextRecognitionScript.chinese);
  String recognizedText = "";
  @override
  void initState() {
    super.initState();
    _initializeCamera(); // for camera initialization
    PaintingBinding.instance.imageCache.maximumSizeBytes = 1024 * 1024 * 2000;
  }

  @override
  void dispose() {
    _cameraController.dispose();
    textDetector.close();
    super.dispose();
  }

  InputImage getInputImage(CameraImage cameraImage) {
    final allBytes = WriteBuffer();
    for (Plane plane in cameraImage.planes) {
      allBytes.putUint8List(plane.bytes);
    }
    final bytes = allBytes.done().buffer.asUint8List();

    final Size imageSize =
        Size(cameraImage.width.toDouble(), cameraImage.height.toDouble());

    final InputImageRotation imageRotation =
        InputImageRotationValue.fromRawValue(
                _cameraController.description.sensorOrientation) ??
            InputImageRotation.rotation0deg;

    final InputImageFormat inputImageFormat =
        InputImageFormatValue.fromRawValue(cameraImage.format.raw) ??
            InputImageFormat.nv21;

    final planeData = cameraImage.planes.map(
      (Plane plane) {
        return InputImagePlaneMetadata(
          bytesPerRow: plane.bytesPerRow,
          height: plane.height,
          width: plane.width,
        );
      },
    ).toList();

    final inputImageData = InputImageData(
      size: imageSize,
      imageRotation: imageRotation,
      inputImageFormat: inputImageFormat,
      planeData: planeData,
    );

    return InputImage.fromBytes(bytes: bytes, inputImageData: inputImageData);
  }

  void _processCameraImage(CameraImage image) async {
// getting InputImage from CameraImage
    InputImage inputImage = getInputImage(image);
    final RecognizedText recognisedText =
        await textDetector.processImage(inputImage);
// Using the recognised text.
    for (TextBlock block in recognisedText.blocks) {
      if (mounted) {
        setState(() {
          recognizedText = "${block.text} ";
        });
      }
    }
    ImageCache _imageCache = PaintingBinding.instance.imageCache;
    _imageCache.clearLiveImages();
    _imageCache.clear();
  }

  void _initializeCamera() async {
    // Get list of cameras of the device
    // List<CameraDescription> cameras = await availableCameras();
    cameras = await availableCameras();

    _cameraController = CameraController(cameras[0], ResolutionPreset.medium);

// Initialize the CameraController
    if (mounted) {
      setState(() {
        _initializeControllerFuture =
            _cameraController.initialize().then((_) async {
          // 保持相機為垂直
          _cameraController
              .lockCaptureOrientation(DeviceOrientation.portraitUp);
          // Start streaming images from platform camera
          await _cameraController.startImageStream((CameraImage image) =>
              _processCameraImage(
                  image)); // image processing and text recognition.
          return;
        }).catchError((Object e) {
          if (e is CameraException) {
            switch (e.code) {
              case 'CameraAccessDenied':
                logger.w('User denied camera access.');
                break;
              default:
                logger.e('Handdle other errors');
                break;
            }
          }
        });
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
        future: _initializeControllerFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.done) {
            logger.i("Show your recognized text $recognizedText");
            return Center(
                child: CameraPreview(
              _cameraController,
              child: Text(
                "Show your recognized text $recognizedText",
                style: const TextStyle(color: Colors.red, fontSize: 24),
              ),
            ));
          } else {
            return const Center(child: CircularProgressIndicator());
          }
        });
  }
}
