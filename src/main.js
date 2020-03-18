import App from './App.svelte';
import './scss/style.scss';

const app = new App({
	target: document.querySelector('.l-container'),
	props: {
		'title': 'COVID-19 Minnesota Cancellations'
	}
});

window.app = app;

export default app;
