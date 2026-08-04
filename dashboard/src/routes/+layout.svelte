<script lang="ts">
	import '../app.css';

	let { children } = $props();
</script>

<svelte:head>
	<title>xoxo wasita — the data</title>
	<meta name="robots" content="noindex, nofollow" />
	<meta
		name="description"
		content="What 57 people said while Wasita defended her dissertation"
	/>
</svelte:head>

{@render children()}
