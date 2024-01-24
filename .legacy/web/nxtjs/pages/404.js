import styleOf from "../components/styleOf.module.css";

export default function ErrorPage() {
	return (
	<div className={styleOf.container}>
		<span className={styleOf.error}>
			404
		</span>
			Error
	</div>
	)
}