import {
	A,Header,WitChoc,BigBoldLetters,ShowThe,Back,ParseMatter
} from "./base.js";
import {
	getPostsMatter
} from "./base2.js";

import styleOf from "../components/styleOf.module.css";

export async function getStaticProps() {
	const postsMatter=getPostsMatter();
	return {
		props: {
			postsMatter,
		},
	};
}

export default function Main({postsMatter}) {
	return (
		<>
			<Header title={["@S","@SitePageName"]}/>
			<WitChoc/>
			
			<div className={styleOf.container}>
				<BigBoldLetters are="Caffeine AUC & Neoguri Logo"/>
				<ShowThe img="/cafe.png"/>
				<ShowThe img="/neoguri.jpg"/>
				<BigBoldLetters are="Static Props"/>
				<ParseMatter of={postsMatter}/>
			</div>
			
			{Back}
		</>
	);
}