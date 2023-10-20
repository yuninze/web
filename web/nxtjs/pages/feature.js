import {
	A,Header,WitChoc,BigBoldLetters,ShowThe,ShowAsListFrom
} from "./front.js"
import styleOf from "../components/styleOf.module.css"
import {useState} from "react"

const SandwichBrands=[
	{name:"M.D.",file:"/mcd.png",enabled:true},
	{name:"M.T.",file:"/mt.png",enabled:true},
	{name:"SUB",file:"/sub.png",enabled:true},
	{name:"B.G.K.",file:"/bk.png",enabled:true},
	{name:"E.M.T.",file:"/em.png",enabled:true},
	{name:"K.F.C.",file:"/kfc.png",enabled:true},
	{name:"SBUX",file:"/sbux.png",enabled:true},
]

function CountButton() {
	const [click,setClick]=useState(0)
	function setSetClick() {
		setClick(click+1)
	}
	function delSetClick() {
		setClick(0)
	}
	return (
		<section>
			<button onClick={setSetClick}>
				{click} times
			</button>
			<button onClick={delSetClick}>
				Delete
			</button>
		</section>
	)
}

function StringForm() {
	const [value,setValue]=useState("")
	function setSetValue(evnt) {
		setValue(evnt.target.value)
	}
	return (
		<>
			<input value={value} onChange={setSetValue}/>
			<button onClick={()=>setValue("")}>Reset</button>
			{value?value.length:"empty"}
		</>
	)
}

function CheckBox() {
	const [checked,setChecked]=useState(false)
	function setSetChecked(evnt) {
		setChecked(evnt.target.checked)
	}
	return (
		<>
			<input type="checkbox" checked={checked} onChange={setSetChecked}/>
			ChkBox:::
			<span>{checked?"true":"false"}</span>
		</>
	)
}

function PushToDraw({from}) {
	function DrawSomethingFrom(the) {
		const DrawRandomInteger=(max)=>(
			Math.floor(Math.random()*max)
		)
		
		return (
			the[DrawRandomInteger(the.length)]
		)
	}
	
	const [drawed,setDrawed]=useState("Nothing")
	function setSetDrawed() {
		setDrawed(DrawSomethingFrom(from))
	}
	
	return (
		<>
			<section>
				<ShowAsListFrom arr={SandwichBrands}/>
			</section>
			<section>
				<button onClick={setSetDrawed}>햄버거집 고르기</button>
				<span>{drawed.name}</span>
			</section>
			<section>
				<ShowThe img={drawed.file} alt={drawed.name}/>
			</section>
		</>
	)
}

function Interactives() {
	return (
		<>
			<BigBoldLetters are="Hamburger on Web"/>
				<PushToDraw from={SandwichBrands}/>
			<BigBoldLetters are="Tests"/>
				<StringForm/>
				<CountButton/>
				<CheckBox/>
		</>
	)
}

export default function FeatureScreen() {
	return (
		<>
			<Header title={["yuninze","features"]}/>
			<WitChoc/>
			<div className={styleOf.container}>
				<section className={styleOf.interactives}>
					<Interactives/>
				</section>
			</div>
		</>
	)
}