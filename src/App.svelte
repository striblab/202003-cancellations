<script>
  import { onMount } from 'svelte';
	import { intcomma } from 'journalize';
  import Event from './Event.svelte'

  // local component variables
  let json = [];
  let backup_timer;
  let filteredEvents;
  let search_term = '';
  let search = false;
  let category_labels = {
    'arts': 'Arts',
    'business': 'Business',
    'concert': 'Concert',
    'free': 'Free services',
    'gov': 'Government',
    'religious': 'Religious',
    'restaurant': 'Restaurants',
    'sports': 'Sports',
    'other': 'Other events',
    'all': 'All'
  }

  let getData = async function() {
		const response = await fetch("https://static.startribune.com/news/projects/all/202003-cancellations/cancellations.json");

		if (response.ok) {
			json = await response.json();
			return json;
		} else {
			backup_timer = setTimeout(getData, 5000);
			return [];
		}
	}

  // props
  export let events;
  export let categories = ['all', 'arts', 'business', 'concert', 'free', 'gov', 'religious', 'restaurant', 'sports', 'other']
  export let checked_cats = [];
  export let scrollY;
  export let y_from_top;

  export const clearFilters = function (event) {
    checked_cats = [];
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

    filteredEvents = events.filter(event => {

      let match = true;
      if (checked_cats.length == 0 || checked_cats == 'all') {
        match = true
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

    console.log(filteredEvents)

    // if (search_term.length > 2) {
    //   search = true
    // }
    // else {
    //   search = false
    // }
    //
    // if (search) {
    //     filteredEvents = events.filter(function(d) {
    //       return d.event_name.includes(search_term)
    //     })
    //     console.log(filteredEvents)
    // }
    //
    // if (checked_cats.length == 0 || checked_cats == 'all') {
    //   filteredEvents = events;
    // }
    // else {
    //   filteredEvents = events.filter(function(d) {
    //     return d.category === checked_cats;
    //   })
    // }
  }

  onMount(async function() {
    getData();
  });

</script>

<div class="search">
  <h3>Search</h3>
  <i class="strib-icon strib-search"></i>
  <input bind:value={search_term} />
</div>

<div class="categorySelector">
  <h3>Select a category</h3>
  {#each categories as category}
    <div class="feature {category}">
      <input type=radio bind:group={checked_cats} value={category} class:all-selected="{categories == checked_cats}">
      <label class="features {category}">{category_labels[category]}</label>
    </div>
  {/each}
</div>

<div class="eventsContainer">
  {#each filteredEvents as event}
    <Event {event}/>
  {/each}
</div>
