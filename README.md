
카카오톡 채널을 이용한 챗봇

[http://pf.kakao.com/\_BNZRb](http://pf.kakao.com/_BNZRb)

[##_Image|kage@bPhDwh/btrS08qmRrL/h3t2CcerH6KePLtgthIF7K/img.png|CDM|1.3|{"originWidth":620,"originHeight":348,"style":"alignLeft","width":363,"height":204}_##]

---

### **1\. 캐릭터 소개**

[##_Image|kage@m72Aa/btrS09bIyIS/vdJOCWHkdeqUjzZP7hPRFK/img.png|CDM|1.3|{"originWidth":1024,"originHeight":1024,"style":"alignLeft","width":253,"height":253,"filename":"DALL&amp;amp;amp;amp;amp;middot;E 2022-11-18 17.17.38 - A very cute counselor seal animation character.png"}_##]

**이름 : 오복이**

**직업 : 심리상담사**

**종류? : 물범**

**"위로봇 오복이"는 인공지능 비서가 아닙니다.**

**오복이는 내가 한 질문에 대해 위로로 답변해주는 감성 대화 챗봇입니다.**

**오복이는 정해진 시나리오로 답변하지 않습니다.(직접구현한 API를 통해 답변합니다.)**

**오복이는 검색시스템을 통해 질문과 가장 유사한 질문을 찾아 그의 해당하는 답변을 해줍니다.** 

#### **TMI**

저 캐릭터 이미지는 Open-AI의 인공지능(DALL-E)이 생성한 이미지입니다.

"애니메이션으로 된 착하고 똑똑한 심리상담가 물범" 이런식으로 생성했던 것 같습니다 ㅋㅋ

\+ 다른 이미지들을 쓰려다가 저작권 문제가 있을까봐 그냥 생성했습니다.

---

### **2.  사용 데이터**

1\. 송영숙 님의 챗봇 데이터

**[https://github.com/songys/Chatbot\_data](https://github.com/songys/Chatbot_data)**

2\. AI-HUB 웰니스 상담 데이터

**[https://aihub.or.kr/opendata/keti-data/recognition-laguage/KETI-02-006](https://aihub.or.kr/opendata/keti-data/recognition-laguage/KETI-02-006)**

3\. AI-HUB 감성대화 말뭉치

[https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=86](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=86) 

위 3가지의 데이터를 종합해서 사용했습니다.

대답이 질문으로 끝나는 경우는 제거하였습니다.

\*싱글턴 대화이기 때문

---

### **3\. 준비물**

1\. 서버

 - 배포를 하려면 서버가 필요한데 일단 구글 클라우드 플랫폼(GCP)의 무료 3개월 크리딧을 사용했습니다.

 - 스펙은 VM인스턴스 : e2-medium

      CPU : 2-core , 메모리 : 4GB

2\. 카카오톡 채널 & 오픈빌더

 - 회원 가입하고 채널 만들고 나면 어느 정도 승인기간이 있었던 것 같습니다.

 - 가입절차 및 채널 생성은 생략하겠습니다..

---

