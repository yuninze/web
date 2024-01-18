import {
	A,Header,WitChoc,BigBoldLetters,ShowThe,Back,ParsePostSpecFrom
} from "./front.js";
import styleOf from "../components/styleOf.module.css";

const imgur=[
	"https://i.imgur.com/"
];
const scientists=[
	{id:"MK3eW3As",name:"Someone",sex:"Male",race:"Alien",desc:["Lovely","Cake"],friends:[1,2,3],fav:false},
	{id:"YfeOqp2",name:"Someone",sex:"Female",race:"Human",desc:["Blue Jello"],friends:[0,5,7],fav:true},
	{id:"QIrZWGIs",name:"Another",sex:"Unknown",race:"Alien",desc:["Red Sea"],friends:[100,5,7],fav:false},
	{id:"yXOvdOSs",name:"Someone",sex:"Male",race:"Human",desc:["Applic Substance"],friends:[2,3,7],fav:true},
	{id:"7vQD0fPs",name:"Someone",sex:"Unknown",race:"Human",desc:["Diasterous Water"],friends:[2,3,7],fav:true},
];

function ShowBy({id,name,sex,race,friends}) {
	if (Array.isArray(friends)) {
		return (
			<article>
				<BigBoldLetters are={name}/>
				<ul>
				{friends.map(friend=>
					<li key={friend}>{friend}</li>)}
				</ul>
			</article>
		);
	} else {
		return (
			"FriendsIsNotAnArrayError"
		);
	}
}

function Show({scientist}) {
	const path=imgur[0]+scientist.id+".jpg";
	return (
		<>
			<ul>
				<li key={scientist.id}>
					<a href={path} target="_blank" rel="noreferrer">
						<img src={path} alt={scientist.name} width="50"/>
					</a>
						<p>
							<b>{scientist.name}</b> ({scientist.sex})
						</p>
				</li>
			</ul>
		</>
	);
}

function IsFav({elem}) {
	const isFav=elem.fav?"✔":"X";
	return (
		<li key={elem.id}>
			<span>{elem.id}:::{isFav}</span>
		</li>
	);
}

function ShowListing({arr}) {
	const Shows=arr.map(elem=>
		<span><Show scientist={elem}/>{elem.desc}</span>
	);
	return (
		<li>{Shows}</li>
	);
}

function ShowProfileOf({scientists}) {
	const size=80;
	const alien=scientists.filter(one=>one.race==="Alien");
	const others=scientists.filter(one=>one.race!=="Alien");
	return (
		<>
			<BigBoldLetters are="Data Listing"/>
			<h4>Alien</h4>
			<ul>
				{alien.map(one=>
					<li className={styleOf.list} key={one.id}>
						<img src={imgur[0]+one.id+".jpg"} alt={one.name} width={size}/>
						<b>{one.name}</b> ({one.sex} {one.race})
					</li>
				)}
			</ul>
			<h4>Others</h4>
			<ul>
				{others.map(one=>
					<li className={styleOf.list} key={one.id}>
						<img src={imgur[0]+one.id+".jpg"} alt={one.name} width={size}/>
						<b>{one.name}</b> ({one.sex} {one.race})
					</li>
				)}
			</ul>
		</>
	);
}

function ShowDescsOf({scientists}) {
	const _descs=[]
	for (const scientist of scientists) {
		const name=scientist.name
		const desc=scientist.desc.join(" ")
		_descs.push(
			<span key={desc}>
				<b>{name}: </b>{desc}
			</span>
		)
		_descs.push(<hr key={desc}/>)
	}
	_descs.pop()
	return (
		<>
		<BigBoldLetters are="Buggy Component"/>
		<ul key="descs">
			{_descs}
		</ul>
		</>
	)
}

export default function ProfilesScreen() {
	return (
		<>
			<WitChoc/>
			<div className={styleOf.container}>
				<ShowProfileOf scientists={scientists}/>
				<ShowDescsOf scientists={scientists}/>
			</div>
		</>
	);
}