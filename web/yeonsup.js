/* destructing assignments */
let q,w,e,r;
[q,w,e,r]=[0,1,2,3];
[q,w,e,r].forEach(console.log);
[q,w,...a]=["q","w","qwer","asdf"]; // a=["qwer","asdf"]

// array.forEach(elem, idx, arr) = applymap
let q=[0,1,2,3];
function muli(elem,idx,arr) {arr[idx]=elem*100;}
q.forEach(addi)

// Variable Scopes가 파이턴과 같음. const는 in-block scope.
if (Math.random()>=.5) {const rnd=">=.5";} else {const rnd="ha";}

// 선언 안됨을 eval.할 수 없고, initialize 안된 건 eval.가능
let x;
x==undefined;

// 램다 이름 넣으면 안됨
(function () {console.log("lambda");})
// 램다 실행
();

// who랑 비슷
globalThis

// const는 reassignment만 막고 mutation은 냅둠
const K={key:"KK"};
K.key="KKK";
const CAF_NAM_ARR=["SBUX"];
CAF_NAM_ARR.push("DICO");

// type conversion, dynamic concat.
let samsung="galaxy buds";
samsung+=" "
samsung+2
parseFloat("1.223455ax");

// indexed array에 없는 elem을 넣을 수 있다. undefined가 아님.
let cnt=[0,/*none*/,2,3,];
cnt[1]

// floating-point literals 파이턴이랑 같음.
[digits].[digits] [(e) [(-|+)] digits]

// Object literals. 바로 attribute처럼 된다. 파이턴처럼 dict key로도 나온다.
let phone={
	apple:["mini","retina"],
	samsung:["note","buds"],}
phone.apple[0]
phone["samsung"][0]

// backtick 
`qwe
rrr`
let q,w=["hi","gogo"];
`${q}..${w}`

// Array.isArray.. 문자열 markdown parsing
if (Array.isArray(obj)) {
	return obj.map((elem) => `* ${elem}`).join("\n");
}

// block statements.. if for while
let arr=[];
while (Math.random()<.9) {arr.push(Math.random());}

if (Math.random()>.5) {
	console.log("gt");
} else {
	console.log("lt");
}

function editCheck() {
	if (obj.length>8) {
		return true;
	} else {
		return false;
	}
}

// 파이턴과 다르게 Boolean 옵젝과 bool type 옵젝이 다름
let boolpy=Boolean(false);

// exception handling
// throw raise
throw {true:{csgo:["exception:csgo",true]}};

// try except else finally, try catch finally
function getMonthName(mo) {
	mo--; // mo를 0..으로 맞춤
	const MO=["Jan","Feb","Mar","Apr"];
	if (MO[mo]) {
		return MO[mo]
	} else {
		throw Error("해당 인덱스의 월 이름 없음");
	}
}

try {
	moName=getMonthName(12);
	} catch (err) {
		moName="없는 월";
		console.log(moName);
		console.error(`에러 있음: ${err.name}: ${err.message}`);
		throw Error("월 이름 없음");
	} finally {
		var resp={finally_resp:"try statement 끝냄"};
}
resp.finally_resp

/*************/
/*************/
for (let start=0; start<3; start++) {
	console.log(`init, cond, do, start=${start}`);
}

let munza="music";
for (let start=0; start<=munza.length; start++) {
	console.log(munza[start]);
}

let rands={rand:[]};
do {rands.rand.push(Math.floor(Math.random()*10));}
while (rands.rand.length<5);

while (rands.rand.length<11) {
console.log("appending");
rands.rand.push("aa");
}
/*************/
/*************/

// continue break 파이턴과 같음
let loopSu=0;
while (true) {
	console.log("azik true");
	loopSu++
	if (loopSu>=10) {
		console.error(`loopSu=${loopSu}`);
		loopSu=0;
		break
	}
}
// ㅎㅎㅎㅎ
let mat={a:["qwer"],b:["asdf"],c:["zxcv"]};
for (const col in mat) {
	console.error(col); // in은 indexㄴ ㅏkey줌
}

// 어트리뷰트로 인식되는 딕셔너리는 이터러블로 하려면 Object.entries(x) 써야함
mat={a:["qwer"],b:["asdf"],c:["zxcv"]};
for (const [col,row] of Object.entries(mat)) {
	console.log(col,row); // 이건 
}

// 튜플은 js 업슴. 그리고 ndarray는 파이턴처럼 이터러블 됨
let ㄴ=[["a",0],["b",1],["nun",2]];
for (const [first,second] of ㄴ) {
	console.log(first,second);
}

// declaring function
function sqrt(num) {
	return num*num;
}
const _sqrt=sqrt(10);

array.map((s)=>s.length)

// for (col,row) in [[],[]]
const [col,row] = [[col],[row]]

// 문자열 접합과 즉할당
let munza="samsung";
munza+="buds";

// status="major" if age>=18 else "major"
// np.where(if, ifVal, elseVal)
let status= age>=18?"major":"minor"

// comma 반복문 조건문에서 변수조작
for (let col=0,idx=0; col<=idx; col++,idx++) {
	console.log(col,idx);
}

// typeof object는 type 문자열로 줌
// isinstance == instanceof
if (string instanceof string) {..}

// js에서 in은 오브젝트나 어트리뷰트 수준으로 판정함
let phones=["samsung","apple","xiaomi"];
0 in phones;
5 in phones;
"xiaomi" in phones;
phones[0]=="samsung"

let dataframe={row:[0,1],col:["a","b"]};
"row" in dataframe;

// self == this
this.propertyName

// new operator to create an instance of a user-defined object

// Date... year, 
let today=new Date();
today=new Date("2000-01-01");
xmas=new Date(1995,11,25); // datetime.datetime(1995,11,25)

// string object is a wrapper
let munza=new String("SOUND CLOUD"); // 이렇게 오브젝트 래퍼 사용 x
munza="dududu";

startsWith, endsWith
munza.includes("du");
munza.indexOf("dudu");
munza.concat(" waratah");
munza.substr(0,6);
toLowerCase,toUpperCase
trim

// array
let arr=new Array();
arr=Array();
arr=[];
for (let elem in arr) {
	console.log(elem);
}
arr.csgo=["eco","full",""]
arr.length==3
arr.length=2

for (start; until; per) {}

arr=["cs","go","fps","game",undefined,,];
arr.forEach((q) => console.error(q));

// np.concatenate, list.extend
arr.concat("apex","over")

// str.join(iterable)
arr.join("_")

// list.append, arr.push -> arr.length
arr.push("counter")

// pop은 파이턴과 다름
arr.pop() // 마지막 엘리먼트를 빼고 줌 mutation

// arr.shift -> pd.shift, mutation
arr.shift() 
arr.unshift("csgo") // pd.shift(1)

// js 인덱싱은 파이턴과 같음 (처음 포함, 끝 포함x)
arr.slice(0,3)

// arr.at -> pd.DataFrame.iat((x,y))
arr.at(-3)

// arr.reverse -> arr.reverse mutation
arr.reverse()

// arr.sort() mutation
arr.sort

// arr.flat -> np.flatten
ndarray([ [] ])

// arr.indexOf(elem) -> index
// lastIndexOf(elem) ->

// arr.splice mutation
arr.splice(start,count)

arr.forEach((elem) => func(elem)) -> elem
arr.map((elem) => elem+"!"); -> arr
arr.filter((elem) => typeof elem == "number"); -> arr

// all, any
arr.every(func->bool)
arr.some(func->bool)

// itertools.groupby
devices=[
{name:"sec",model:"mini"},
{name:"sec",model:"note"},
{name:"apple",model:"buds"},
{name:"apple",model:"test"},
];
forEach((q) => console.error(q));
forEach((q) => console.error(q.model));

for (let q=0; q<=devices.length; q++) {
	console.log(q);
} // for q in range(q)
for (const elem of devices) {
	console.log(`elem.name=${elem.name}`);
} // for..of는 옵젝의 properties를 줌
for (const q in devices) {
	console.log(devices[q].name);
} // for..in은 옵젝의 element를 줌

// set
let ㅅㅌ=new Set();
ㅅㅌ.add(elem)
ㅅㅌ.has(elem)
ㅅㅌ.delete(elem)
ㅅㅌ.size

// typeof
typeof 12345==="number";

let obj;
if (age>=18) {
	obj={hello:"adult"};
}
obj={
	name:"obj",
	age:"age",
	model:"dict",
};

// 이런 식으로도 컨스트럭팅 가능
function device(brand,model) {
	this.brand=brand;
	this.model=model;
	this.type="dict";
}
let p=new device("apple","mini");


// 오버로딩
let game={
	title:"csgo",
	genre:"fps",
	spec:"high"
};
let play={
	title:"soft",
	genre:"gameplay",
	spec:"bad"
};

function show() {
console.log(`title is ${this.title}, genre is ${this.genre}.`);
}

game.show=show;
play.show=show;





















