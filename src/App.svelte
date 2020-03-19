<script>
  import { onMount } from 'svelte';
	import { intcomma } from 'journalize';
  import Event from './Event.svelte'
  import json from './data/cancellations.json'

  // local component variables
  // let json = [];
  let backup_timer;
  let filteredEvents;
  let search_term = '';
  let search = false;
  let category_labels = {
    'arts': 'Arts',
    'business': 'Business',
    'concert': 'Concerts',
    'free': 'Free services',
    'gov': 'Government',
    'grocery': 'Groceries',
    'pharm': 'Pharmacies',
    'religious': 'Religious',
    'restaurant': 'Restaurants',
    'sports': 'Sports',
    'other': 'Other',
    'all': 'All'
  }

  function detach(node) {
    node.parentNode.removeChild(node);
  }

  // let getData = async function() {
	// 	const response = await fetch("https://static.startribune.com/news/projects/all/202003-cancellations/cancellations.json")
  //
	// 	if (response.ok) {
	// 		json = await response.json();
	// 		return json;
	// 	}
  //   else {
	// 		backup_timer = setTimeout(getData, 5000);
	// 		return [];
	// 	}
	// }

  // props
  export let events;
  export let categories = ['all', 'arts', 'business', 'concert', 'free', 'gov', 'grocery', 'pharm','religious', 'restaurant', 'sports', 'other']
  export let closed = ['Suspended/Postponed', 'Cancelled', 'Closed']
  export let open = ['Open', 'Other']
  export let checked_cats = 'all';
  export let checked_status = 'Open';
  export let scrollY;
  export let y_from_top;

  export const clearFilters = function() {
    checked_cats = [];
    checked_status = [];
  }

  $: {
    let happy = scrollY;
    if (checked_cats != 'all' || checked_cats.length != 0) {
      y_from_top = document.querySelector('.l-container').getBoundingClientRect().top;
    } else {
      y_from_top = 8675309;
    }
  }

  // reactive variables
  $: {
    events = json.filter(function(d) {
      return d.category !== 'k12_school' || d.category !== 'college'
    })
    events = events.reverse();

    // if (search_term.length == 0) {
    //   clearFilters()
    // }

    filteredEvents = events.filter(event => {
      let match = true;

      if (checked_status == 'All' && checked_cats == 'all') {
        match = true;
      }
      else if (checked_status == 'Closed' && open.includes(event.status)) {
        match = false;
      }
      else if (checked_status == 'Open' && closed.includes(event.status)) {
        match = false;
      }
      else if (checked_cats != 'all' && event.category != checked_cats) {
  			match = false;
  		}

      let search_blob = event.event_name + ' ' + event.city + ' ' + event.venue;
      if (search_term != '' && search_blob.toLowerCase().indexOf(search_term.toLowerCase()) === -1) {
  			match = false;
  		}
  		return match;
    })

  }

  // onMount(async function() {
  //   getData();
  // });

</script>

<div class="search">
  <h3>Search</h3>
  <i class="strib-icon strib-search"></i>
  <input bind:value={search_term} />
</div>

<div class="statusFilter">
  <h3>Open or closed?</h3>
  <div class="feature">
    <input type=radio bind:group={checked_status} value="All">
    <label class="features all">All</label>
  </div>
  <div class="feature">
    <input type=radio bind:group={checked_status} value="Open" checked>
    <label class="features Open">Open</label>
  </div>
  <div class="feature">
    <input type=radio bind:group={checked_status} value="Closed">
    <label class="features Closed">Closed</label>
  </div>
</div>

<div class="categorySelector">
  <h3>Filter results by category</h3>
  {#each categories as category}
    <div class="feature {category}">
      <input type=radio bind:group={checked_cats} value={category} class:all-selected="{categories == checked_cats}">
      <label class="features {category}">{category_labels[category]}</label>
    </div>
  {/each}
</div>

<div class="eventsContainer">
  {#if filteredEvents.length == 0}
    <p class="noResults">No results</p>
  {:else}
    {#each filteredEvents as event}
      <Event {event}/>
    {/each}
  {/if}
</div>

<!-- <section id="credits">
		<p>Data compiled by Star Tribune staff</p>
		<p>Design and development by Thomas Oide</p>
</section> -->
