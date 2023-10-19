import {
	A,Header,WitChoc,BigBoldLetters,ShowThe,ShowAsListingFrom
} from "./front.js"
import styleOf from "../components/styleOf.module.css"
import {useState} from "react"

const SandwichBrands=[
	{name:"맥 도널드",enabled:true},
	{name:"맘스터치",enabled:true},
	{name:"서브웨이",enabled:true},
	{name:"B.G.K.",enabled:true},
	{name:"E.M.T.",enabled:true},
	{name:"K.F.C.",enabled:true},
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
	const [value,setValue]=useState(null)
	function setSetValue(evnt) {
		setValue(evnt.target.value)
	}
	return (
		<>
			<input value={value} onChange={setSetValue}/>
			<button onClick={()=>setValue("")}>Reset</button>
			{value?value.length:"null value"}
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
			plcHldrChkBox:::
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
			the[DrawRandomInteger(the.length)].name
		)
	}
	
	const [drawed,setDrawed]=useState("Nothing")
	function setSetDrawed() {
		setDrawed(DrawSomethingFrom(from))
	}
	return (
		<>
			<p>
				<button onClick={setSetDrawed}>PTD</button>
				<span>was {drawed}</span>
			</p>
		</>
	)
}

function Interactives() {
	return (
		<>
			<StringForm/>
			<CountButton/>
			<CheckBox/>
			<PushToDraw from={SandwichBrands}/>
		</>
	)
}

export default function RequestsScreen() {
	return (
		<>
			<Header title={["yuninze","Requests"]}/>
			<WitChoc/>
			<div className={styleOf.interactives}>
				<Interactives/>
			</div>
		</>
	)
}