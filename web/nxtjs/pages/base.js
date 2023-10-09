import Head from "next/head";
import A from "next/link";
import Image from "next/image";

import styleOf from "../components/styleOf.module.css";

function Header({title}) {
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

const WitChoc=()=>{
	const WitChocLogo=<Image src="/logo.png" width="180" height="115"/>;
	const WitChocLogoYeopChar=<span className={styleOf.WitChocLogoYeopChar}>Placeholder: Welcome Testers</span>;
	const Menu=({name,goes})=>(
		<span className={styleOf.WitChocMenu}>
			<A href={goes}>
				{name}
			</A>
		</span>
	);
	return (
		<div>
			{WitChocLogo}{WitChocLogoYeopChar}
			<div className={styleOf.WitChocMenuWitChoc}>
			<Menu name="Main" goes=""/>
			<Menu name="Intro" goes="/sx"/>
			<Menu name="Request" goes="/sx"/>
			<Menu name="Contact" goes="/sx"/>
			<Menu name="Back" goes="/"/>
			</div>
		</div>
	);
}

const BigBoldLetters=({are,goto})=>{
	const hasGoto=goto?goto:false;
	if (hasGoto) {
		return (
			<A href={goto}>
				<h3>{are}</h3>
			</A>
		);
	} else {
		return (
				<h3>{are}</h3>
		);
	}
}

const ShowThe=({img})=>(<A href={img}><Image src={img} alt="" height={230} width={330}/></A>);

const Back=(<span className={styleOf.Back}><A href="/">Back</A></span>);

const ParseMatter=({of})=>(
	<ul>
		{of.map(({id,date,title})=>(
			<li className={styleOf.list} key={id}>{date} - {title} ({id})</li>
		))
		}
	</ul>
);

export {
	A,Header,WitChoc,BigBoldLetters,ShowThe,Back,ParseMatter
}