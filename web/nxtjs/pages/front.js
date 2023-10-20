import Head from "next/head";
import A from "next/link";
import Image from "next/image";
import styleOf from "../components/styleOf.module.css";

const OriginUrl="/";

export function Header({title}) {
	if (Array.isArray(title)) {
		title=title.join(" - ");
	}
	return (
		<Head>
			<link rel="icon" href="favicon.ico"/>
			<title>{title}</title>
		</Head>
	);
}

export const WitChoc=()=>{
	const WitChocLogo=(
		<Image src="/logo.png" alt="logo" width={120} height={80}/>
	)
	const WitChocLogoYeopChar=(
		<span className={styleOf.WitChocLogoYeopChar}>Yun Inze</span>
	)
	const Menu=({name,goes})=>(
		<span className={styleOf.WitChocMenu}>
			<A href={goes}>
				{name}
			</A>
		</span>
	);
	return (
		<>
			{WitChocLogo}{WitChocLogoYeopChar}
			<div className={styleOf.WitChocMenuWitChoc}>
			<Menu name="Intro" goes={OriginUrl}/>
			<Menu name="Display" goes="/monitor"/>
			<Menu name="Feature" goes="/feature"/>
			</div>
		</>
	);
}

export const BigBoldLetters=({are,goto})=>{
	const hasGoto=goto?goto:false;
	if (hasGoto) {
		return (
			<A href={goto}>
				<h3>{are}</h3>
			</A>
		)
	} else {
		return (
			<h3>{are}</h3>
		)
	}
}

export function ShowThe({img,about}) {
	const HasAlt=about?about:"alt Placeholder"
	return (
		<Image src={img} alt={HasAlt} width={200} height={200}/>
	)
}

export const ParsePostSpecFrom=({of})=>(
	<ul>
		{of.map(({id,date,title})=>(
			<li className={styleOf.list} key={id}>
				<A href={`/posts/${id}`}>
				{title} <span>{id}</span> {date} 
				</A>
			</li>
		))}
	</ul>
)

export function ShowAsListFrom({arr}) {
	return (
		arr.map(elem=>
			<span className={styleOf.test}>
				{elem.name}, </span>
		)
	)
}