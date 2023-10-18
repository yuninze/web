import {
	A,Header,WitChoc,BigBoldLetters,ShowThe,Back,ParsePostSpecFrom
} from "./front.js";
import {
	getPostsSpec
} from "./back.js";
import styleOf from "../components/styleOf.module.css";

export async function getStaticProps() {
	const postsSpecs=getPostsSpec();
	return {
		props: {
			postsSpecs,
		},
	};
}

export default function IndexScreen({postsSpecs}) {
	return (
		<>
			<Header title={["yuninze","pgName"]}/>
			<WitChoc/>
			
			<div className={styleOf.container}>
				<BigBoldLetters are="Caffeine AUC & Neoguri Logo"/>
				<ShowThe img="/cafe.png"/>
				<ShowThe img="/neoguri.jpg"/>
				<BigBoldLetters are="Static Props"/>
				<ParsePostSpecFrom of={postsSpecs}/>
			</div>
		</>
	);
}