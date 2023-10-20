import {
	A,Header,WitChoc,BigBoldLetters,ShowThe,Back,ParsePostSpecFrom
} from "./front.js"
import {
	getPostsSpec
} from "./back.js"
import styleOf from "../components/styleOf.module.css"

export async function getStaticProps() {
	const postsSpecs=getPostsSpec();
	return {
		props: {
			postsSpecs,
		},
	}
}

export default function IndexScreen({postsSpecs}) {
	return (
		<>
			<Header title={["yuninze","test-dev-build"]}/>
			<WitChoc/>
			
			<div className={styleOf.container}>
				<BigBoldLetters are="Profile"/>
				<ShowThe img="/yiz.jpg"/>
				<BigBoldLetters are="Related Props"/>
				<ParsePostSpecFrom of={postsSpecs}/>
			</div>
		</>
	)
}