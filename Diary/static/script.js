/* script.js */

/*
전체 불빛(작은 불빛 + 큰 불빛) 갯수를 count 변수에 담음
큰 불빛 갯수를 blurCount 변수에 담음
html에서 stage class 선택해서 stage 변수에 담음
*/
const count     = 80;
const blurCount = 50;
const stage = document.querySelector(".stage");

/*
- for문(반복문)으로 count 숫자보다 작을 시 makeLight() 함수 실행
- 첫 시작 후 10 * i (count 보다 작은 수)만큼 밀리초(ms)가 지나야 실행됨
- JS 내장함수인 setTimeout에 화살표함수를 적용하여
  함수를 파라미터로 전달하여 한번 실행 후 종료
*/
for (let i = 0; i < count; i++) {
  setTimeout(() => {
    makeLight(i);
  }, 10 * i);
}

/*
- for문안에서 makeLight() 함수가 한번 종료되면 다시 실행이 안되어서
  반복해서 실행시키려 timer 변수로 감싸고 반복 실행인 setInterval 적용
- 실행 시 설정해준 시간(초) 뒤에 count 보다 미만인 갯수에
  makeLight() 함수가 한번 실행되고
  setInterval로 주어진 시간(초)동안 반복해서 실행
*/
const timer = setInterval(() => {
  for (let i = 0; i < count; i++) {
    setTimeout(() => {
      /*
      makeLight() 함수를 setinterval로 반복 실행 시
      실행과 동시에 생성한 span tag를 함수가 종료될때 html에서 삭제해줘야
      span tag가 반복적으로 계속 무한으로 생성되지 않음
      */
      const removespan = document.querySelector("span");
      removespan.parentNode.removeChild(removespan);
      // 삭제와 동시에 함수가 실행되면서 html에 span tag 생성됨
      makeLight(i);
    }, 10 * i);
  }
  /* timer에서 생성된 불빛들은 시작시 5초 뒤에 나타남*/
  /* 위에 변수에 담지 않은 for문으로 불빛을 먼저 보여주고
     for문에 setTimeout이 종료될때쯤 timer변수 지연시간이 끝나서 불빛이 나타나고
     종료되면 span tag를 삭제하고 다시 생성하면서 무한 반복됨
  */
}, 5000);


// makeLlight() 함수로 큰 별, 작은 별 만들기
function makeLight(i) {
  /*
  [1] 불빛을 먼저 생성
      함수 실행 시 span tag 생성하고
      if문(조건문)으로 큰 불빛(blurCount)에 넣어준 숫자보다 작으면
      span tag에 blur class 추가함
      stage 클래스 하위에 span 태그 연결
  */
  let span = document.createElement("span");
  if (i < blurCount) {
    span.classList.add("blur");
  }
  stage.appendChild(span);

  /*
  [2] 불빛 애니메이션 설정
      불빛에 애니메이션 주기 전에 기본 셋팅 설정
      가로 위치 랜덤, 세로 위치 랜덤
      크기 스케일 값으로 랜덤
      투명값을 0으로 먼저 안보이게 설정
  */
  gsap.set(span, {
    left: gsap.utils.random(0, stage.offsetWidth),
    top: gsap.utils.random(0, stage.offsetHeight),
    scale: gsap.utils.random(0.2, 1.2, 0.1),
    opacity: 0
  });

  // [3] 애니메이션 효과를 적용할 타임라인 생성
  let tl = gsap.timeline({
    paused: true,          // 자기 자신을 가리킴
    onComplate: () => {    // onComplate 함수를 하나 만들어서
                           // 익명함수로 식별자를 값으로 전달
      span.remove();       // span tag 삭제
      makeLight(i);        // makeLight() 함수 실행
    }
  })

  /*
  [4] if문(조건문)으로 큰 불빛, 작은 불빛 만들어서
      불빛이 움직이고, 사라지게 만들기
  */
  if (i < blurCount) {
    /*
    [4-1] 큰 불빛 생성
          큰 불빛 투명도
          지속 시간 (초)
    */
    tl.to(span, {
      opacity: gsap.utils.random(0.1, 0),
      duration: .8
    })
    /*
    [4-2] 불빛 움직임
          큰 불빛 x, y축 움직임 (80px 안에서 랜덤값을 생성하여 움직임)
          불빛 유지 지속시간 (나타났다가 자연스럽게 사라짐)
          애니메이션 스타일 (기본스타일 Power0.easeNone)
          사라지는 시간 (초)
    */
    tl.to(span, {
      y: gsap.utils.random(-80, 80),
      x: gsap.utils.random(-80, 80),
      duration: gsap.utils.random(4, 2, 3),
      ease: Power0.easeNone
    }, -0.3)
    /*
    [4-3] 불빛 사라짐
          투명값 0으로 설정
          .8(초) 동안 자연스럽게 나타남
          마지막에 적용된 애니메이션(여기서는 duration: .8)의
          마지막 종료전에 0.8초 추가 (딜레이를 주어서 자연스럽게 사라짐)
    */
    tl.to(span, {
      opacity: 0,
      duration: .8
    }, ">-0.8")

    // [4-4] 불빛 애니메이션 실행
    tl.play();

  // else 로 불빛 하나 더 생성
  } else {
    /*
    [4-5] 작은 불빛 생성
          작은 불빛 투명도를 낮추지 않게 적용해야 빛이남
          지속 시간 (초)
    */
    tl.to(span, {
      opacity: gsap.utils.random(1, 1),
      duration: .3
    })
    /*
    [4-6] 불빛 움직임
          작은 불빛 x, y축 움직임
          (지정한 픽셀 안에서 랜덤값을 생성하여 움직임)
          지속시간을 조금 길게 적용하고
          사라지는 시간을 짧게 적용해서 반짝이게 만듬
    */
    tl.to(span, {
      x: gsap.utils.random(-100, 100),
      y: gsap.utils.random(-100, 100),
      duration: gsap.utils.random(4, 2, 5),
      ease: Power0.easeNone
    }, -0.3)
    /*
    [4-7] 불빛 사라짐
          여기서 opacity를 .3으로 준 이유는
          작은 불빛이 사라지면서 정지되게 만들기 위함
          0으로 주게되면 갑자기 뿅 하고 사라져서
          0.1초 사이에 새로 나타나는 불빛하고 자연스럽게 이어지지 않음
    */
    tl.to(span, {
      opacity:  .3,
      duration: .3
    }, ">-0.3")
    // [4-8] 불빛 애니메이션 실행
    tl.play();
  }
}