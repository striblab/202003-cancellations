<script>
  import { onMount } from 'svelte';
	import { intcomma } from 'journalize';
  import Event from './Event.svelte'
  import json from './data/public_cancellations.json'

  // local component variables
  // let json = [];
  let backup_timer;
  let filteredEvents;
  let openFilteredEvents;
  let closedFilteredEvents;
  let search_term = '';
  let search = false;
  let category_labels = {
    'arts': 'Arts',
    'business': 'Business',
    'concert': 'Concerts',
    'farm': 'Farms/Farmers Markets',
    'gov': 'Government',
    'grocery': 'Groceries',
    'mall': 'Malls',
    'pharm': 'Pharmacies',
    'volunteer': 'How to help',
    'restaurant': 'Restaurants',
    'sports': 'Sports',
    'other': 'Other',
    'all': 'All'
  }
  let area_labels = {
    'tc': "Twin Cities",
    'greater_mn': "Greater Minnesota",
    'wisc': "Wisconsin"
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
  export let search_timeout;
  export let previous_search_term = '';
  export let categories = ['all', 'arts', 'business', 'concert', 'farm', 'gov', 'grocery', 'mall', 'pharm', 'restaurant', 'sports', 'volunteer', 'other']
  // export let closed = ['Suspended/Postponed', 'Cancelled', 'Closed']
  // export let open = ['Open', 'Other']
  export let checked_cats = 'all';
  export let checked_status = 'All';
  export let checked_area = 'all';
  export let scrollY;
  export let y_from_top;
  export let open_loc = [];
  export let closed_loc = [];
  export let tc_ev = [];
  export let greater_mn_ev = [];
  export let wisc_ev = [];
  // export let art = [];

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
      return d.publish === 'yes';
    })
    // events = events.reverse();

    open_loc = events.filter(function(d) {
      return d.status == 'Open' || d.status == 'Other';
    })

    closed_loc = events.filter(function(d) {
      return d.status === 'Closed' || d.status === 'Cancelled' || d.status === 'Suspended/Postponed';
    })

    tc_ev = events.filter(function(d) {
      return d.location === 'tc';
    })

    greater_mn_ev = events.filter(function(d) {
      return d.location === 'greater_mn';
    })

    wisc_ev = events.filter(function(d) {
      return d.location === 'wisc';
    })

    // art = events.filter(function(d) {
    //   return d.category === 'arts';
    // })

    // console.log(open_loc)
    // console.log(closed_loc)

    if (checked_status == 'Open') {
      openFilteredEvents = open_loc.filter(event => {
        let match = true;

        if (checked_cats == 'all') {
          match = true;
        }
        else if (checked_cats != 'all' && event.category != checked_cats) {
      		match = false;
      	}

        let location = event.location;
          if (checked_area != 'all' && location.toLowerCase().indexOf(checked_area.toLowerCase()) === -1) {
            match = false
          }

        let search_blob = event.event_name + ' ' + event.city + ' ' + event.venue;
          if (search_term != '' && search_blob.toLowerCase().indexOf(search_term.toLowerCase()) === -1) {
      			match = false;
      		}
      	return match;
      });

    }
    else if (checked_status == 'Closed') {
      closedFilteredEvents = closed_loc.filter(event => {
        let match = true;

        if (checked_cats == 'all') {
          match = true;
        }
        else if (checked_cats != 'all' && event.category != checked_cats) {
      		match = false;
      	}

        let location = event.location;
          if (checked_area != 'all' && location.toLowerCase().indexOf(checked_area.toLowerCase()) === -1) {
            match = false
          }

        let search_blob = event.event_name + ' ' + event.city + ' ' + event.venue;
          if (search_term != '' && search_blob.toLowerCase().indexOf(search_term.toLowerCase()) === -1) {
      			match = false;
      		}
      	return match;
      });
    }
    else if (checked_status == 'All') {
      filteredEvents = events.filter(event => {
        let match = true;

        if (checked_cats == 'all') {
          match = true;
        }
        else if (checked_cats != 'all' && event.category != checked_cats) {
      		match = false;
      	}

        let location = event.location;
          if (checked_area != 'all' && location.toLowerCase().indexOf(checked_area.toLowerCase()) === -1) {
            match = false
          }

        let search_blob = event.event_name + ' ' + event.city + ' ' + event.venue;
          if (search_term != '' && search_blob.toLowerCase().indexOf(search_term.toLowerCase()) === -1) {
      			match = false;
      		}
      	return match;
      });
    }

    // filteredEvents = events.filter(event => {
    //   let match = true;
    //
    //   if (checked_status == 'All' && checked_cats == 'all') {
    //     match = true;
    //   }
    //   else if (checked_status == 'Closed' && open.includes(event.status)) {
    //     match = false;
    //   }
    //   else if (checked_status == 'Open' && closed.includes(event.status)) {
    //     match = false;
    //   }
    //   else if (checked_cats != 'all' && event.category != checked_cats) {
  	// 		match = false;
  	// 	 }
    //
    //   let search_blob = event.event_name + ' ' + event.city + ' ' + event.venue;
    //   if (search_term != '' && search_blob.toLowerCase().indexOf(search_term.toLowerCase()) === -1) {
  	// 		match = false;
  	// 	}
  	// 	return match;
    // })

  }

  const logStatusClick = function (event) {
		window.gtag("event", "Status selected", {'event_category': 'Cancellations/Openings', 'event_label': event.target.value});
	}

  const logCatClick = function (event) {
		window.gtag("event", "Category selected", {'event_category': 'Cancellations/Openings', 'event_label': event.target.value});
	}

  const logSearch = function (event) {
		clearTimeout(search_timeout);
		search_timeout = setTimeout(function () {
			if (event.target.value != previous_search_term) {
				previous_search_term = event.target.value;
				window.gtag("event", "Event search", {'event_category': 'Cancellations/Opening', 'event_label': event.target.value});
			}
		}, 1000);
	}

  onMount(() => {
    window.dataLayer = window.dataLayer || [];
	  function gtag(){dataLayer.push(arguments);}
		window.gtag = gtag;
	  gtag('js', new Date());
	  gtag('config', 'UA-114906116-1');
  });

</script>

<div class="search">
  <h3>Search</h3>
  <i class="strib-icon strib-search"></i>
  <input placeholder="ex: Duluth" bind:value={search_term} on:keyup={logSearch}/>
</div>

<div class="statusFilter">
  <h3>Open or closed?</h3>
  <div class="feature">
    <input type=radio bind:group={checked_status} value="All" on:click={logStatusClick}>
    <label class="features all">All</label>
  </div>
  <div class="feature">
    <input type=radio bind:group={checked_status} value="Open" on:click={logStatusClick}>
    <label class="features Open">Open</label>
  </div>
  <div class="feature">
    <input type=radio bind:group={checked_status} value="Closed" on:click={logStatusClick}>
    <label class="features Closed">Closed</label>
  </div>
</div>

<div class="statusFilter">
  <h3>Area</h3>
  <div class="feature">
    <input type=radio bind:group={checked_area} value="all" on:click={logStatusClick}>
    <label class="features all">All</label>
  </div>
  <div class="feature">
    <input type=radio bind:group={checked_area} value="tc" on:click={logStatusClick}>
    <label class="features all">Twin Cities</label>
  </div>
  <div class="feature">
    <input type=radio bind:group={checked_area} value="greater_mn" on:click={logStatusClick}>
    <label class="features Open">Greater Minnesota</label>
  </div>
  <!-- <div class="feature">
    <input type=radio bind:group={checked_area} value="wisc" on:click={logStatusClick}>
    <label class="features Closed">Wisconsin</label>
  </div> -->
</div>

<div class="categorySelector">
  <h3>Filter results by category</h3>
  {#each categories as category}
    <div class="feature {category}">
      <input type=radio bind:group={checked_cats} value={category} on:click={logCatClick}>
      <label class="features {category}">{category_labels[category]}</label>
    </div>
  {/each}
</div>

<p class="lastUpdated">Last updated: {events[0].last_update}</p>

<div class="eventsContainer">

  {#if checked_status === 'Open'}
    {#if checked_cats !== 'all'}
      {#each openFilteredEvents as event}
        <Event {event}/>
      {/each}
    {:else if openFilteredEvents.length == 0}
      <p class="noResults">No results</p>
    {:else}
      {#each openFilteredEvents as event}
        <Event {event}/>
      {/each}
    {/if}
  {:else if checked_status === 'Closed'}
    {#if checked_cats !== 'all'}
      {#each closedFilteredEvents as event}
        <Event {event}/>
      {/each}
    {:else if closedFilteredEvents.length == 0}
      <p class="noResults">No results</p>
    {:else}
      {#each closedFilteredEvents as event}
        <Event {event}/>
      {/each}
    {/if}
  {:else if checked_status === 'All'}
    {#if checked_cats !== 'all'}
      {#each filteredEvents as event}
        <Event {event}/>
      {/each}
    {:else if filteredEvents.length == 0}
      <p class="noResults">No results</p>
    {:else}
      {#each filteredEvents as event}
        <Event {event}/>
      {/each}
    {/if}
  {/if}

</div>

<!-- <section id="credits">
		<p>Data compiled by Star Tribune staff</p>
		<p>Design and development by Thomas Oide</p>
</section> -->
