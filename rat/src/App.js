import "./style.css";
/* import {object} from "./objects.js"; */
/* import {something} from "./something.js"; */

const imgur=[
	"https://i.imgur.com/",
];
const scientists=[
	{id:"MK3eW3As",desc:"hell",fav:false},
	{id:"QIrZWGIs",desc:"lllo",fav:true},
	{id:"YfeOqp2",desc:"hell",fav:true}
];

function Face({img}) {
	const path=imgur[0]+img.id+".jpg";
	return (
		<a href={path} target="_blank" rel="noreferrer">
			<img src={path} alt={img.desc} width="150"/>
		</a>
	);
};

function IsFav({elem}) {
	return (
		<span>{elem.id} {elem.fav&&"✔"}</span>
	);
};

function ListingImages({arr}) {
	const images=arr.map(elem=><Face img={elem}/>);
	return (
		<div>
			<li>{images}</li>
		</div>
	);
};

function Main() {
	return (
		<div>
			<h3>Baseline</h3>
			<li>
				<Face img={scientists[0]}/>
				<IsFav elem={scientists[0]}/>
			</li>
			<li>
				<Face img={scientists[1]}/>
				<IsFav elem={scientists[1]}/>
			</li>
			<li>
				<Face img={scientists[2]}/>
				<IsFav elem={scientists[2]}/>
			</li>
				<h3>ListingImages</h3>
				<ListingImages arr={scientists}/>
		</div>
	);
};

export default Main