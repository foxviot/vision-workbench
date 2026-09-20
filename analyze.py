import argparse
import json
import time
from pathlib import Path
import cv2
import numpy as np


def analyze(source, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    if source:
        frame = cv2.imdecode(np.fromfile(source, dtype=np.uint8), cv2.IMREAD_COLOR)
        if frame is None:
            raise ValueError('Cannot decode input image')
    else:
        frame = np.full((480, 720, 3), 245, np.uint8)
        cv2.rectangle(frame, (60, 80), (240, 270), (90, 110, 220), -1)
        cv2.circle(frame, (420, 210), 90, (190, 120, 60), -1)
        cv2.rectangle(frame, (510, 340), (650, 420), (70, 180, 120), -1)
    started = time.perf_counter()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    annotated = frame.copy()
    for contour in sorted(contours, key=cv2.contourArea, reverse=True):
        if cv2.contourArea(contour) < 100:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        boxes.append(dict(x=x, y=y, width=w, height=h, area=cv2.contourArea(contour)))
        cv2.rectangle(annotated, (x, y), (x+w, y+h), (20, 180, 50), 2)
        cv2.putText(annotated, str(len(boxes)), (x, max(20, y-8)), cv2.FONT_HERSHEY_SIMPLEX, .7, (10, 100, 30), 2)
    report = dict(method='Canny + external contours; not semantic object detection',
                  width=frame.shape[1], height=frame.shape[0], regions=boxes,
                  processing_ms=round((time.perf_counter()-started)*1000, 3))
    for name, image in [('input', frame), ('edges', edges), ('annotated', annotated)]:
        ok, encoded = cv2.imencode('.png', image)
        if not ok:
            raise RuntimeError('PNG encoding failed')
        encoded.tofile(str(output / (name + '.png')))
    (output / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Local edge and region analysis')
    parser.add_argument('--input', help='Optional image; omitted = generated shapes demo')
    parser.add_argument('--output', default='examples/output')
    args = parser.parse_args()
    analyze(args.input, args.output)
