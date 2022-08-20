# Posenet-pytorch를 돌려보고, 이를 ROS 노드로 제작해보았다.

- Posenet-pytorch : https://github.com/youngguncho/PoseNet-Pytorch
- Posenet-pytorch-ROS : https://github.com/cwha0212/PoseNet-Pytorch-ROS

---

우선 시작하기에 앞서 정말로 ~~초짜티 엄청나는 코드다.~~
그래도... 내힘으로 처음 만들어본 나름 의미있는 Node이기 때문에 어느정도 설명을 하는게 좋을 것 같았다.

- Posenet-pytorch
  - 특정 건물 혹은 위치의 사진과 각 사진을 찍은 6-DOF를 Quaternion으로 표현한 값을 Data로 활용하여 현재의 6-DOF를 사진으로 특정해 주는 모델이다.
  - training을 통해 .pth파일을 얻을 수 있으며, 이를 활용하여 예측을 할 수 있다.
  - 이 과정을 python의 라이브러리중 하나인 pytorch를 활용, 현재의 pose를 알아낸다 해서 Posenet-pytorch라 이름지은것 아닐까... ~~얕디얕은 지식의 한계~~

이런 코드를 실행해보고, 얻은 한가지의 .pth파일을 활용하여 Node를 제작하였다.

---

간략하게 패키지구성을 보면

- `node_solver.py`
- `node_data_loader.py`
- `node_model.py`
- `node_pose_utils.py`
- `image_publish.py`
- `Posenet_pytorch_node.py`
- `model/best_net.pth`
- `image/test.png`

로 구성이 되어있다. 앞에 **node_** 가 붙은 4개의 파일은 기존에 있던 파일에서 내가 원하는 부분만 추출하고, 또 몇가지 argument를 다른것으로 대체하여 만들었다. 큰 틀만 살펴보면

- `image_path`,`metadata_path`같은 경우에는 원래 python에서 `metadata_path`의 파일을 읽고, 그 해당 파일에 적혀진 정보를 토대로 `image_path`의 사진을 불러오는 방식 이었다면, 나는 경로 지정을 하지 않고 바로 이미지를 불러오는 방식을 선택하였다. 그래서 본인의 파일을 보면 `image`라는 argument가 있는것을 확인할 수 있다.
- `model`은 **Resnet** 으로 고정하였다. 이는 차후에 수정한다면 할 수 있을지도...
- `mode`는 **test** 로 고정하였다. 어차피 이미 training은 완료된 상태에서 사진을 받았을 때 6-DOF를 보내는 것이 목표이기 때문에, test만 남겨도 충분하다고 판단하였다.
- 이외의 값은 왠만해서는 default값을 따라가도록 하였다.

원래 있던 파일과 비교를 해본다면 상당부분을 날려버린 것을 확인할 수 있다. ~~이게 다 나의 뇌용량 한계~~ 최대한 필요하다고 생각한 부분만 최소한으로 남긴 것이고, 추가로 수정할 여지는 충분히 있다.

---

## image_publish.py

말 그대로 이미지를 publish하는 node이다. msg의 경우 `sensor_msgs/Image.msg`를 사용하였다. 해당 msg를 사용하기 위해서 변환과정이 필요하였는데

1. opencv로 이미지 불러오고
2. cvbridge로 imgmsg로 변환
3. msg에 저장시키고 publish

하는 과정을 거쳤다. 이 node는 말도 쉽고, 실제로 코드도 상당히 간단하다.

---

## Posenet_pytorch_node.py

이번에 만든 Main이 되는 node이다. 이미지를 subscribe 한 뒤에 이를 처리해서 `geometry_msgs/Pose.msg`에 값을 입력하는 것 까지 만들었다.(publish 해서 받을 node는 따로 만들지 않았다.) 여기서도 `Image.msg`를 사용하기위해 변환과정이 필요하였는데

1. cvbridge로 cv2로 변환
2. cv2형식의 이미지 데이터를 BGR에서 RGB형태로 변환
3. 이를 PIL이미지에서 사용하지 위해 `Image.fromarray(cvt_img)`

를 해주면 사용할 준비가 다 되었다. ~~이렇게 한 이유는 원래 코드에서 PIL를 사용했기 때문이다.~~
후에 밑에줄 부터는 `test.py`의 main 함수 부분을 가져왔고, 데이터들을 pos, ori에 반환 받은 후 각 Pose의 값에 넣어주었다. 이렇게 msg가 완성되고, 나는 출력하는 것 까지만 실행하였다.

---

## data_publish.py

데이터 시각화를 위해서 사용한 데이터의 ground truth 값을 추출하고 전송하는 node이다. `geometry_msgs/Pose.msg`를 publish한다.

---

## rviz.py

마찬가지로 데이터 시각화를 위해 사용한 node이다. `visualization_msgs/Marker.msg`를 사용하였고, Arrow형태를 사용하였다. posenet_pytorch를 사용하여 생성된 Pose추측값과 ground truth값을 각각 초록, 파랑으로 설정하였다.

![스크린샷1](/image/Resnet_34.png)
![스크린샷2](/image/rqt_graph.png)