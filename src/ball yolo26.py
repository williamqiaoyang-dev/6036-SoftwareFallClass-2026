from ultralytics import YOLO # type: ignore

model = YOLO("yolo26n.yaml")
results = model.train(data="model/data.yaml", epochs=20, imgsz=512)