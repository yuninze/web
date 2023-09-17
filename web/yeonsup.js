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

// 루프
for (let start=0; start<3; start++)
	console.log(`init, cond, do, start=${start}`);

let munza="music";
for (let start=0; start<=munza.length; start++)
	console.log(munza[start]);

let rands={rand:[]};
do rands.rand.push(Math.floor(Math.random()*10));
while (rands.rand.length<5);

while (rands.rand.length<11) {
console.log("appending");
rands.rand.push("aa");
}
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







