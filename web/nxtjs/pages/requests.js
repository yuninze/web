import {
	A,Header,WitChoc,BigBoldLetters,ShowThe,Back,
} from "./front.js"
import styleOf from "../components/styleOf.module.css"
import {useState} from "react"

const SandwichBrands=[
	{name:"맘스 터치",enabled:true},
	{name:"맥 도널드",enabled:true},
	{name:"맥 오더",enabled:true},
	{name:"K.F.C.",enabled:true},
	{name:"서브웨이",enabled:true},
	{name:"B.G.K.",enabled:true},
	{name:"E.M.T.",enabled:true},
]

function Interactives() {
	const [count,setCount]=useState(null)
	const [picked,pick]=useState(null)
	const RandomInteger=(max)=>{
		return Math.floor(Math.random()*max)
	}
	const PickSomething=(from)=>{
		const RandomNumber=RandomInteger(from.length)
		return from[RandomNumber].name
	}
	return (
		<>
			<section>
				<ShowThe img="/ngr.png"/>
				<ShowThe img="/lotty.png"/>
				<ShowThe img="/neoguri.jpg"/>
			</section>
			<section>
				골라진 숫자
				<button onClick={()=>setCount(RandomInteger(SandwichBrands.length))}>실행</button>
				<button onClick={()=>setCount(null)}>
				삭제</button>
				<span>{count}</span>
			</section>
			<section>
				골라진 밥집
				<button onClick={()=>pick(PickSomething(SandwichBrands))}>실행</button>
				<button onClick={()=>pick(null)}>삭제</button>
				<span className={styleOf.answer}>{picked}</span>
			</section>
		</>
	)
}

export default function RequestsScreen() {
	return (
		<>
			<Header title={["yuninze","Requests"]}/>
			<WitChoc/>
			
			<div className={styleOf.container}>
				<Interactives/>
			</div>
		</>
	)
}