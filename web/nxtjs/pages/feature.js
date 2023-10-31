import {
	A,Header,WitChoc,BigBoldLetters,ShowThe,ShowAsListFrom
} from "./front"
import styleOf from "../components/styleOf.module.css"
import {useState} from "react"
import {things} from "./tobuy"

const SandwichBrands=[
	{name:"MD",file:"/mcd.png",enabled:true},
	{name:"MT",file:"/mt.png",enabled:true},
	{name:"SUB",file:"/sub.png",enabled:true},
	{name:"BGK",file:"/bk.png",enabled:true},
	{name:"EMT.",file:"/em.png",enabled:true},
	{name:"KFC",file:"/kfc.png",enabled:true},
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
				Clicked {click} Times
			</button>
			<button onClick={delSetClick}>
				Delete
			</button>
		</section>
	)
}

function ActionButton({label,count,onClick}) {
	return (
		<>
			<button onClick={onClick}>
				{label}
			</button>
		</>
	)
}

function ActionButtonStateShared() {
	const [count,setCount]=useState(0)
	
	return (
		<section>
			<ActionButton label="addi" count={count} onClick={()=>setCount(count+1)}/>
			<ActionButton label="addi" count={count} onClick={()=>setCount(count+1)}/>
			<ActionButton label="reset" count={count} onClick={()=>setCount(0)}/>
			<p>
				{count}
			</p>
		</section>
	)
}

function StringForm() {
	const [value,setValue]=useState("")
	function setSetValue(evnt) {
		setValue(evnt.target.value)
	}
	return (
		<section>
			<input value={value} onChange={setSetValue}/>
			<button onClick={()=>setValue("")}>Reset</button>
			{value?value.length:"empty"}
		</section>
	)
}

function CheckBox() {
	const [checked,setChecked]=useState(false)
	function setSetChecked(evnt) {
		setChecked(evnt.target.checked)
	}
	return (
		<section>
			<input type="checkbox" checked={checked} onChange={setSetChecked}/>
			ChkBox 
			<span style={{color: checked?"black":"red"}}> {checked?"true":"false"}</span>
		</section>
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
	
	const [drawed,setDrawed]=useState("None")
	function setSetDrawed() {
		setDrawed(DrawSomethingFrom(from))
	}
	
	let Drawed
	if (drawed==="None") {
		Drawed=(
			<>
				Nothing Been Drawed
			</>
			)
	} else {
		Drawed=<ShowThe img={drawed.file} alt={drawed.name}/>
	}
	
	return (
		<article>
			<section>
				<button onClick={setSetDrawed}>고르기</button>
				<span>{drawed.name}</span>
			</section>
			<section>
				{Drawed}
			</section>
		</article>
	)
}

function ShowBrands({expr}) {
	return (
		<section>
			<BigBoldLetters are={expr+": "+SandwichBrands.length}/>
			<ShowAsListFrom arr={SandwichBrands}/>
		</section>
	)
}

export default function FeatureScreen() {
	return (
		<>
			<Header title={["yuninze","features"]}/>
			<WitChoc/>
			<div className={styleOf.container}>
				<section className={styleOf.interactives}>
					<BigBoldLetters are="State-shared Counter"/>
				<ul>
					<ActionButtonStateShared/>
				</ul>
					<BigBoldLetters are="Things"/>
					<ShowAsListFrom arr={things}/>
					<BigBoldLetters are="Draw Brand"/>
				<ul>
					<PushToDraw from={SandwichBrands}/>
				</ul>
					<BigBoldLetters are="Others"/>
					<StringForm/>
					<CheckBox/>
				</section>
			</div>
		</>
	)
}