/** 클래스 모음 **/
class Brand{
	constructor(name="걸포동 레스토랑",history=[],id=[]){
		const nameLocIndex=name.indexOf("동 ");
		if (nameLocIndex<0) {
			name=`모르겠는동 ${name}`;
		}
		this.name=name;
		this.loc=name.substring(0,nameLocIndex+1).trim();
		this.nick=name.substring(nameLocIndex+2).trim();
		this.history=history;
		this.id=id;
	}
	addHistory(dt){
		this.history.push(dt);
	}
	addId(id){
		this.id.push(id);
	}
	getCount(){
		return this.history.length;
	}
}

/** 변수 모음 **/
const 트플=new Brand("걸포동 트리플 에이");
const 스벅=new Brand("걸포동 스벅");
const 메가=new Brand("걸포동 메가 커피");
const 마그=new Brand("걸포동 마스그레이");
const 투썸=new Brand("걸포동 투썸 플레이스");
const 산책=new Brand("걸포동 산책");
var Brands_=Array(트플,스벅,메가,마그,투썸,산책);

/** 함수 모음 **/
function init(jsonData) {
	// 루트에 있는 카페 제인슨을 로드합니다
	var latestBrands=new Array();
	const l=jsonData.length;
	for (q=0;q<l;q++) {
		latestBrands.push(new Brand(name=jsonData[q].name,history=jsonData[q].history));
	}
	return latestBrands;
}
function jg(){
	// 런타임 일시를 스트링으로 냅니다
	const 지금=new Date();
	return `${지금.getFullYear()}-${지금.getMonth()+1}-${지금.getDate()} ${지금.getHours()}:${지금.getMinutes()}`;
}
function mr(){
	// 장전된 브랜드와 개수를 냅니다
	const brand=latestBrands.map(({name})=>name);
	const msg=`지금 ${brand.join(", ")}의 ${brand.length}개 브랜드가 있습니다.`;
	console.log(msg);
	return msg;
}
function most(){
	// 지금껏 가장 많이 걸린 브랜드를 냅니다
	const historyCount=latestBrands.map(({history})=>history.length);
	const historyCountLargest=Math.max.apply(null,historyCount);
	if (historyCountLargest<1) {
		const msg=`고르기를 한 적이 없습니다.`;
		return msg;
	}
	const historyCountLargestIndex=historyCount.indexOf(historyCountLargest);
	const historyCountLargestBrand=latestBrands[historyCountLargestIndex].name;
	const msg=`${historyCountLargestBrand}가 가장 많이 걸렸습니다. 지금껏 ${historyCountLargest}번 걸렸습니다.`;
	console.log(msg);
	return msg;
}
function hist(){
	// 각 브랜드가 언제 걸렸었는지 냅니다.
	const latestBrandsLength=latestBrands.length;
	const msgs=[];
	var brandHistoricalCount=0;
	for (q=0;q<latestBrandsLength;q++) {
		const name=latestBrands[q].name;
		console.log(`${name}`);
		if (latestBrands[q].history.length==0) {
			var msg=(`${name}는 걸린 적 없습니다.`);
		} else {
			const hist=latestBrands[q].history.join(", ");
			var msg=(`${name}는 ${hist}에 걸렸습니다.`);
			brandHistoricalCount+=1
		}
		msgs.push(msg);
	}
	console.log(`${brandHistoricalCount}개 브랜드가 걸렸었습니다.`);
	return msgs.join("<br/>");
}

function sel(){
	// 장전된 브랜드 중 하나를 고릅니다
	const rand=Math.floor(Math.random()*latestBrands.length);
	const brand=latestBrands[rand];
	brand.addHistory(jg());
	brand.addId(genId(1));
	const msg=`갈 곳은 ${brand.name}(위치는 ${brand.loc})입니다. 지금껏 ${brand.getCount()}번 걸렸습니다.`;
	const historyId=brand.id;
	console.dir(historyId);
	return msg;
}
function clean(id){
	// 변형을 없앱니다
	document.getElementById(id).value="";
	console.log(`${id}의 변형을 없앴습니다.`);
}
function nb(){
	// 새로운 브랜드를 넣습니다
	const newBrand=document.getElementById("nb").value;
	const brandNames=latestBrands.map(({name})=>name).join();
	if (newBrand=="") {
		var msg=`아무것도 입력되지 않았습니다.`;
	} else if (brandNames.includes(newBrand.slice(-3))) {
		var msg=`이미 있는 브랜드입니다.`;
	} else {
		latestBrands.push(new Brand(newBrand));
		var msg=`${newBrand}를 넣었습니다.`;
	}
	clean("nb");
	console.log(msg);
	return msg;
}
function genId(numericInput) {
	// Epoch와 들어온 숫자 기반으로 시리얼 넘버를 냅니다
	var epochTime=new Date().getTime();
	var randomId=Math.floor(Math.random()*512);
	epochTime=epochTime+numericInput;
	return epochTime+randomId;
}
function jsonlocal(constArray=null){
	// 컨스트렉로 어레이 제이슨 파일을 읽거나, 컨스트럭터 어레이를 제이슨 파일로 씁니다
	if (!constArray) {
		// constArray false면 제이슨 파일을 읽습니다
		if (!Fs.existsSync(jsonFile)) {
			const jsonData=JSON.stringify(Brands_,null,2);
			Fs.writeFileSync(jsonFile,jsonData);
			console.log("제이슨 파일이 없어서 새로 썼습니다.");
		} else {
			const jsonData=JSON.parse(Fs.readFileSync(jsonFile).toString());
			const jsonDataLength=jsonData.length;
			for (q=0;q<jsonDataLength;q++){
			// 제이슨 파일을 그대로 읽으면 클래스로 되지 않으므로 new로 넣습니다
			latestBrands[q]=new Brand(name=jsonData[q].name,history=jsonData[q].history);
			}
			console.log("제이슨 파일을 읽었습니다.");
			return latestBrands;
		}
	} else {
		// constArray true면 제이슨 파일을 씁니다
		const jsonData=JSON.stringify(constArray,null,2);
		Fs.writeFileSync(jsonFile,jsonData);
		console.log("제이슨 파일로 썼습니다.");
	}
}

/** 명령 모음 **/
(async () => {
    latestBrands = await cafeJsonData();
})();