var Engine = Matter.Engine,
  World = Matter.World,
  MouseConstraint = Matter.MouseConstraint,
  Mouse = Matter.Mouse,
  Bodies = Matter.Bodies,
  Composite = Matter.Composite,
  Runner = Matter.Runner;

let engine;
let world;
let letters = [];
let ground;
let mConstraint;
let basket;
let basketDepth = 5;
let maxLettersInBasket = 15;
let bgImage;

let allConsonants = ['여편네', '한녀', '나쁜년', '흑형', '쪽바리', '조선족', '짱개', '깜둥이', '죽어', '쓰레기', '병신', '찌질', '맘충', '애새끼', '창녀', '걸레', '군바리', '매국노', '급식충', '틀딱충', '개저씨', '중2병'];
let sizes = [10, 13, 15, 20, 25];

let years = Array.from({ length: 18 }, (_, i) => 2006 + i); // 2006년부터 2023년까지
let colors = ['#8B7773', '#33FF57', '#3357FF', '#F333FF', '#FF3380', '#33FFF8', '#F8FF33', '#FF8333', '#B833FF', '#FF33F8', '#FF3380', '#33FF80', '#3380FF', '#8033FF', '#FF3380', '#80FF33', '#F833FF', '#FF3380'];

// 여성/가족, 악플/욕설, 인종/국적 퍼센트 데이터 (각각 연도별로 배열 형태)
let womenFamilyPercentages = [3.49, 2.79, 1.63, 1.63, 1.44, 2.4, 3.68, 1.15, 1.63, 0.67, 1.15, 0.75, 2.21, 1.54, 1.35, 3.17, 1.15, 1.23];
let hateSpeechPercentages = [46.13, 36.06, 22.98, 36.15, 33.94, 38.56, 43.11, 48.46, 51.44, 49.71, 50.87, 53.96, 50.67, 48.65, 47.6, 49.33, 55.19, 55.47];
let raceNationalityPercentages = [4.62, 2.4, 2.4, 1.63, 1.73, 4.33, 3.96, 3.46, 3.37, 4.23, 3.65, 1.51, 4.9, 6.06, 8.17, 11.25, 6.63, 4.91];

let currentYearIndex = 0;
let intervalId;
let isPause = false;
let letterIntervals = [];

function preload() {
  bgImage = loadImage('city.png'); // Load the background image
}

function setup() {
  createCanvas(400, 400);
  
  engine = Engine.create();
  world = engine.world;

  var options = {
    isStatic: true
  }
  ground = Bodies.rectangle(200, height, width, 10, options);
  World.add(world, ground);

  let basketWidth = 200;
  basketLeft = Bodies.rectangle(200 - basketWidth / 2, height / 2, basketWidth, basketDepth, options);
  basketRight = Bodies.rectangle(200 + basketWidth / 2, height / 2, basketWidth, basketDepth, options);
  
  // Rotate the slopes to create the sloped roof effect
  Matter.Body.rotate(basketLeft, -PI / 6);
  Matter.Body.rotate(basketRight, PI / 6);

  // 가운데를 막는 투명한 벽 추가
  basketCenter = Bodies.rectangle(200, height / 2 - 40, 30, basketDepth, options);

  World.add(world, [basketLeft, basketRight, basketCenter]);

  let mouse = Mouse.create(canvas.elt);
  mouse.pixelRatio = pixelDensity(); // for retina displays etc
  let options2 = {
    mouse: mouse
  }
  mConstraint = MouseConstraint.create(engine, options2);
  World.add(world, mConstraint);

  startLetterIntervals(); // 첫 번째 연도 시작
  intervalId = setInterval(changeYear, 1000); // 1초마다 년도 변경

  let runner = Runner.create();
  Runner.run(runner, engine);
}

function draw() {
  background(51);
  image(bgImage, 0, 0, width, height); // Draw the background image

  colorMode(HSB);
  fill( currentYearIndex*20,100, 70);
  textSize(12); // 크기에 맞게 텍스트 크기 조정
  textAlign(CENTER, TOP);
  text(years[currentYearIndex], width / 2, 10);
  Engine.update(engine);

  for (let i = letters.length - 1; i >= 0; i--) {
    let letter = letters[i];
    letter.show();
    if (letter.body.position.x < 0 || letter.body.position.x > width) {
      World.remove(world, letter.body);
      letters.splice(i, 1);
    }
  }

  if (basketLeft && basketRight) {
    showBasket();
    checkBasket();
  }
}

function createLetter() {
  if (isPause) return;

  let size = random(sizes);
  let char = random(allConsonants);

  let x;
  do {
    x = random(width / 3, (width * 2) / 3); // 글자가 무작위로 떨어지도록 수정
  } while (x > width / 2 - 10 && x < width / 2 + 10); // 정 가운데에서는 생성되지 않도록 함

  let y = 50;

  letters.push(new Letter(x, y, char, size, color(currentYearIndex*20,100, 70)));
}

class Letter {
  constructor(x, y, char, size, color) {
    let options = {
      frictionAir: 0.1,
      restitution: 0.9
    };
    this.body = Bodies.circle(x, y, size / 2, options);
    this.char = char;
    this.size = size;
    this.color = color;
    Matter.Body.setVelocity(this.body, { x: random(-0.25, 0.25), y: random(0, 0.25) });
    Matter.Body.setAngularVelocity(this.body, random(-0.025, 0.025));
    World.add(world, this.body);
  }

  show() {
    let pos = this.body.position;
    let angle = this.body.angle;
    push();
    translate(pos.x, pos.y);
    rotate(angle);
    textSize(this.size);
    textAlign(CENTER, CENTER);
    fill(this.color);
    text(this.char, 0, 0);
    pop();
  }
}

function showBasket() {
  if (!basketLeft || !basketRight) return; // Add this check

  let posLeft = basketLeft.position;
  let posRight = basketRight.position;

  push();
  colorMode(RGB)
  fill(127);
  rectMode(CENTER);
  // Draw left slope
  push();
  translate(posLeft.x, posLeft.y);
  rotate(-PI / 6);
  rect(35, 0, 180, basketDepth);
  pop();
  // Draw right slope
  push();
  translate(posRight.x, posRight.y);
  rotate(PI / 6);
  rect(-35, 0, 180, basketDepth);
  pop();
  pop();
}

function checkBasket() {
  if (!basketLeft || !basketRight || !basketCenter) return; // Add this check

  let count = 0;
  let basketY = height / 2; // Use the y position of the basket
  let basketLeftX = basketLeft.position.x - 50; // Adjust based on basket width and position
  let basketRightX = basketRight.position.x + 50;
  for (let letter of letters) {
    let pos = letter.body.position;
    let speed = letter.body.speed;
    if (pos.x > basketLeftX && pos.x < basketRightX && pos.y < basketY && speed < 0.7) {
      count++;
    }
  }
  if (count >= maxLettersInBasket) {
    World.remove(world, [basketLeft, basketRight, basketCenter]);
    basketLeft = null;
    basketRight = null;
    basketCenter = null;
  }
}

function changeYear() {
  isPause = true;
  stopLetterIntervals();

  setTimeout(() => {
    currentYearIndex = (currentYearIndex + 1);
    if (currentYearIndex >=  2024) {
      currentYearIndex = 2024
    }
    
    isPause = false;
    startLetterIntervals(); // 새로운 연도에 맞게 글자 생성 속도 조정
  }, 50); // 0.05초간 쉬는 시간
}

function startLetterIntervals() {
  stopLetterIntervals(); // 기존의 인터벌 제거
  letterIntervals = [];

  // 모든 퍼센트 데이터를 합산하여 비율을 조정
  let totalPercentage = womenFamilyPercentages[currentYearIndex] + hateSpeechPercentages[currentYearIndex] + raceNationalityPercentages[currentYearIndex];
  let interval = mapPercentageToInterval(totalPercentage);

  letterIntervals.push(setInterval(createLetter, interval));
}
function mapPercentageToInterval(percentage) {
  // 2018년 이후에는 글자가 더 많이 나오도록 인터벌을 조정합니다.
  const baseYear = 2018;
  const yearFactor = currentYearIndex + 2006 >= baseYear ? 0.75 : 1; // 2018년 이후에는 0.75배 빠르게 생성

  // 퍼센트를 기반으로 인터벌 시간을 계산합니다. 퍼센트가 높을수록 인터벌이 짧아져 글자가 빨리 생성됩니다.
  const maxInterval = 500; // 최대 인터벌 (ms)
  const minInterval = 50; // 최소 인터벌 (ms)
  const scaleFactor = (maxInterval - minInterval) / 100;

  return (maxInterval - (percentage * scaleFactor)) * yearFactor;
}

function stopLetterIntervals() {
  // 기존의 인터벌 제거
  letterIntervals.forEach(interval => clearInterval(interval));
  letterIntervals = [];
}