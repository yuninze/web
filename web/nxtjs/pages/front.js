import Head from "next/head";
import A from "next/link";
import Image from "next/image";

import styleOf from "../components/styleOf.module.css";

const originUrl="http://localhost:3000/";

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
	const WitChocLogo=<Image src="/logo.png" width={110} height={70}/>;
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
			<Menu name="Main" goes={originUrl}/>
			<Menu name="Request" goes="/profiles"/>
			<Menu name="Contact" goes="/profiles"/>
			<Menu name="Back" goes="/"/>
			</div>
		</div>
	);
}

export const BigBoldLetters=({are,goto})=>{
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

export const ShowThe=({img})=>(
	<A href={img}>
		<Image src={img} alt="" height={230} width={330}/>
	</A>
);

export const Back=(
	<span className={styleOf.Back}>
		<A href="/">Back</A>
	</span>
);

export const ParsePostSpecFrom=({of})=>(
	<ul>
		{of.map( ({id,date,title}) => (
			<li className={styleOf.list} key={id}>
				<A href={`/posts/${id}`}>
				{title} <span>{id}</span> {date} 
				</A>
			</li>
		))}
	</ul>
);