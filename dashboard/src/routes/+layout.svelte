<script lang="ts">
	import '../app.css';

	let { children } = $props();
</script>

<svelte:head>
	<title>xoxo wasita 💜 — the data</title>
	<link
		rel="icon"
		href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='0.9em' font-size='90'>💜</text></svg>"
	/>
	<meta name="robots" content="noindex, nofollow" />
	<meta
		name="description"
		content="What 57 people said while Wasita defended her dissertation"
	/>
</svelte:head>

{@render children()}
