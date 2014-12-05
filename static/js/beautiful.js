/*
 *
 * Beautiful.js: The backend of the frontend of courseapp.me
 *	
 * Makes everything Beautiful
 * Copyright CourseApp.me by Paul D'Amora
 * Last updated: November 12, 2014
*/

//Define GLOBAL variables
var oldsubjects = "";
var oldlevels = "";
var olddays = "";

//Only run all of this jazz when the document is ready
$( document ).ready(function() {
	/*
	 * Hides flashed messages
	*/
	//Listens for clicks on flsshed messages
	$('.flashes li').bind('click', function() {
		//Hide the li that was clicked
		$(this).fadeOut();
	});
	
	
	/*
	 * Set options for jquery modal windows
	*/
	$.modal.defaults = {
		overlay: "#000",        // Overlay color
		opacity: 0.1,           // Overlay opacity
		zIndex: 1000,           // Overlay z-index.
		escapeClose: true,      // Allows the user to close the modal by pressing `ESC`
		clickClose: true,       // Allows the user to close the modal by clicking the overlay
		closeText: 'Close',     // Text content for the close <a> tag.
		closeClass: '',         // Add additional class(es) to the close <a> tag.
		showClose: true,        // Shows a (X) icon/link in the top-right corner
		modalClass: "modal",    // CSS class added to the element being displayed in the modal.
		spinnerHtml: null,      // HTML appended to the default spinner during AJAX requests.
		showSpinner: true,      // Enable/disable the default spinner during AJAX requests.
		fadeDuration: null,     // Number of milliseconds the fade transition takes (null means no transition)
		fadeDelay: 1.0          // Point during the overlay's fade-in that the modal begins to fade in (.5 = 50%, 1.5 = 150%, etc.)
	};
	
	
	/*
	 * Activate the tooltipster pluging
	*/
	function start_tooltipster() {
		$('.tooltip').tooltipster({
			maxWidth: 270,
			position: 'right'
		});
		$('.help').tooltipster( {
			theme: 'tooltipster-help',
			maxWidth: 200
		});
	}
	//Call the function
	start_tooltipster();
	
	
	/*
	 * Adds labelFocus class to input labels on login and registration pages
	*/
	
	//For form inputs
	//Check if it was autofilled
	$('form :input').change(function () {
        if($(this).val().length != 0) {
        	$('label').addClass('labelFocus');
        }
    });

	//When a form input is focused by the user
	$("form :input").focus(function() {
		//We add the labelFocus class to that inputs label
		$("label[for='" + this.id + "']").addClass("labelFocus");
	
	//And when that input is blurred 
	}).blur(function() {
		//And if the input is still empty i.e. the user entered nothing
		if( $(this).val().length === 0 ) {
			//We remove the labelFocus class
	    	$('label').removeClass('labelFocus');
	    }//endif
	});//end event listener for from :input focus and blur
	
	
	
	/*
	 * Listens for dropmenu li clicks and checks or unchecks the associated checkbox accordingly
	*/
	
	//Checkboxes
	$( ".dropdown-menu li" ).click(function() {
		//If the li input just clicked is unchecked
		if($(this).find("input").prop("checked") == false) {
			//Set it to checked
			$(this).find("input").prop("checked", true);
		
		//Else if the li input is checked already
		} else  if($(this).find("input").prop("checked") == true){
			//Set it to unchcekd
			$(this).find("input").prop("checked", false);
		}//end if
	});//end event listener form li.click
	
	
	/*
	 * Searches for mathces in the #dropdown-1 dropdown with user input in #dropsearch
	 * Filters out anything that doesn't match
	 * Shows and hides 'x' button on search bar
	*/
	
	//Dropdown Search
	$( "#dropsearch" ).on('input', function() {
		//Flag for whether the subject contain the search term
		var isFound;
		
		//The user has typed something so show the x if the input still has a value
		if($('#dropsearch').val()) {
			$('.x').show();
		} else {
			$('.x').hide();
		}
		
		
		//Loop through every li in the dropdown
		$('#dropdown-1 .dropdown-menu li').each(function(){
			
			//Only continue if the li contains a span element (which will contain the text of the subject name)
			//This makes sure we ignore the dropdown search itself
			if($(this).find("span").length) {
				//Set the isFound flag depending on whether the search term was found
				//-1 will return if not found, and the index will return if it was found
				isFound = $(this).find('span').text().toLowerCase().indexOf($('#dropsearch').val().toLowerCase());
				
				//If the search term was not found, hide it
				if(isFound == -1) {
					$(this).hide();
				//Else show it
				//It will be shown by default, so this is redundant probably
				//But no real harm
				} else {
					$(this).show();
				}
			}
		});
	});
	
	//The event listener for when the user clicks the dropdown search 'X'/erase button
	$('.x').bind('click', function() {
		//Empty the input
		$("#dropsearch").val('');
		
		//Hide the 'x'
		$('.x').hide();
		
		//And show ALL of the li's
		$('#dropdown-1 .dropdown-menu li').each(function(){
			$(this).show();
		});//end loop
	});//end event listener for '.x'.click
	
	/*
	 * Controls range sliders for the sort bar
	*/
	if($('.slider').length) {
		$(function() {
			//Attach the slider to our .slider class
			//And initiate the function
	    	$('.slider').noUiSlider({
				start: [0, 16],
				connect: true,
				range: {
					'min': 0,
					'max': 16
				}
			});
			
			//Watch for when the slider handles lose focus so we can grab the new slider values
			$('.noUi-handle').focusout(function() {
				console.log($('.slider').val());			
			});
	    });
	}
	
	/*
	 * +++++ The AJAX for CourseApp.me +++++
	 * +++++ Contains all functions that are passed to JSON +++++
	 * adlskfjdslfkjdasflkdsjfdsfdsfj++++++THIS IS WHERE THE MAGIC HAPPENS++++++lakdfjdafkldsjflasjadfk
	*/

	
	/*
	 * Listens for clicks on the add to worksheet button and the sends that data to JSON
	*/
	//We need to define this as a function so we can call it everytime something AJAXy happens
	function changeWorksheet() {
		
		//Event handler for a click on a td addto element
		$('td.addto').bind('click', function() {
			//Store the plus and minus in variables for later use
			var thisPlus = $(this).find('.plus');
			var thisMinus = $(this).find('.minus');
			
			// Check and see it the crn is already in the worksheet
			// If it is the .plus class shouldn't exist (it'll be .minus instead)
			if(thisPlus.length) {
				
				//First add the new class
				thisPlus.addClass('minus').removeClass('plus');
				
				//Send the value of the crn to the worksheet
				$.getJSON($SCRIPT_ROOT + '/_worksheet', {
					crn: thisPlus.attr('name')
			    }, function(data) {
				    //console.log(data.crn);
				    //Add new html
				    $("#worksheet").html(data.worksheet);
				    
				    //Reload tooltipster
				    start_tooltipster();
				    
			    });//end .getJSON
			
			//Otherwise we want to remove that crn from the worksheet
		    } else {
		    
		    	//First add the new class
		    	thisMinus.addClass('plus').removeClass('minus');
		    		    	
		    	//Send the value of the crn to remove to the worksheet
			    $.getJSON($SCRIPT_ROOT + '/_worksheet', {
				    crn: 'False',
				    minus_crn: thisMinus.attr('name')
			    }, function(data) {
			    	//console.log(data.crn);
			    	//Add new html
			    	$("#worksheet").html(data.worksheet);
			    	
			    	//Reload tooltipster
			    	start_tooltipster();
			    	
			    });//end .getJSON
		    }
		}); //end event listener for add to worksheet button
	} //end function definition for changeWorksheet
	
	//Call the function we just defined
	changeWorksheet();
	
	
	/*
	 * Gets the value of a query variable (likely the q variable from searching since we hide most other variables)
	*/
	function getQueryVariable(variable) {
        var query = window.location.search.substring(1);
        var vars = query.split("&");
        for (var i=0;i<vars.length;i++) {
            var pair = vars[i].split("=");
            if(pair[0] == variable){return pair[1];}
        }
        return(false);
    }
	
	/*
	 * Sends the next page to json
	 * Pagination via ajax woo
	*/
	function paginateAjax() {
		$('a[page_location]').bind('click', function() {
			
			//Send the number of the page button that was clicked to JSON
			//Also sends all filters to JSON
			$.getJSON($SCRIPT_ROOT + '/_paginate', {
				old_s: oldsubjects,
				old_level: oldlevels,
				old_day: olddays,
				next_page: $(this).attr('page_location'),
				query: getQueryVariable("q")
	    	}, 
	    	//Update the courseContents and pagination with the new rendered pages
	    	function(data) {
		    	//Update courseContents and .pagination html
		    	$("#courseContents table tbody").html(data.filtered_list);
		    	$("#courseContents .pagination").html(data.pagination);
		    	
		    	//We have to recursively call paginateAjax() because we are updating the pagination html
		    	//We do this in EVERY JSON function
		    	paginateAjax(); 
		    	start_tooltipster();
		    });//end function
		    return false;
		});//end event listener for a[page_location].click
	}//end function paginateAjax()
	
	//Call the function we just defined which initiates the event listener
	$(paginateAjax());
	
	/* ++++++++++++++++++++++++++++++++++++++++++++
	 * All code for sending subject filters to json
	 * ++++++++++++++++++++++++++++++++++++++++++++
	*/
	$(function() {
		
		//Define variables
		//These are all global to THIS function
		var subjectClicked = false;
		var replaceString;
		
		//Set the ajaxLoad element
		//This element will display a loading image if ever necessary
		$( "#ajaxLoad" ).width($('#courseContents table').width()).height(300).offset($("#courseContents table").offset());
		
		//Set ALL to checked by default
		$("#dropdown-1 .dropdown-menu li input[id=ALL]").prop("checked",true);
		
		/* 
		 * Listens for the first click in the subject dropdown
		 * - Unchecks all checkboxes except the one clicked
		 * - Adds ALL subject values to oldsubjects variable, then proceeds to unchecked event listener
		 * - and removes the subject value of the selected subject
		*/

		//Event listener mentioned above
		//Calls the addAllSubjects() function
		$('#dropdown-1 .dropdown-menu li').one('click', function() {
			//False by default, true if this function has already ran once
			//Otherwise it would run once for EACH li element
			//So the .one() is not really necessary and serves no purpose
			//Just semantics
			if(!subjectClicked) {
				
				//We want to exclude the dropdown search box, only include checkboxes
				if($(this).find('input').attr("id") != 'dropsearch') {
					//Uncheck all checkboxes
					$("#dropdown-1 .dropdown-menu li input").prop("checked", false);
					//Recheck THIS checkbox
					$(this).find("input").prop("checked", true);
					
					//Empty the oldsubjects variable
					oldsubjects = "";
					
					//Add all subjects (including THIS) to oldsubjects
					$('#dropdown-1 .dropdown-menu li input:checkbox').each(function(){
						oldsubjects = oldsubjects + "," + $(this).val();					
					});//endloop
					
					//Turn on the clicked flag
					subjectClicked = true;
				}//endif
			}//endif (!subjectClicked)
		});//end function 		
				
		/*
		 * Listens for all clicks on li elements
		 * Adds and removes appropriate values from filter list
		 * Sends to JSON
		 * And replaces courseContents and .pagination with new page renders
		*/
		$('#dropdown-1 .dropdown-menu li').bind('click', function() {
			
			// Only keep runnning if the li does not contain dropsearch (our searchbox)		
			if($(this).find('input').attr("id") != 'dropsearch') {
				
				//Only run this is the input that was clicked is now unchecked
				//Meaning it was checked, but not anymore
				//So we're going to want to stop showing its subject
				if($(this).find("input").prop("checked") == false) {
					//Check if nothing is checked now
					//If returns true then we're going to want to check NONE
					if(!$('#dropdown-1 .dropdown-menu li input:checkbox:checked').length) {
						//Go ahead and check NONE
						$('#dropdown-1 .dropdown-menu li input[id=NONE]').prop("checked",true);			
					}//endif (nothing is checked)
						
		    		//Send oldsubjects and the new subject to JSON to filter out
		    		$.getJSON($SCRIPT_ROOT + '/_course_args', {
		    			old_s: oldsubjects,
		    			old_level: oldlevels,
		    			old_day: olddays,
			    		new_s: $(this).find("input").val(),
			    		query: getQueryVariable("q")
			    	}, 
			    	//Receive data from JSON and append to page
			    	//Plus update the oldsubjects variable
			    	function(data) {
				    	oldsubjects = data.subjects;
				    	//$('#result').text(oldsubjects)
				    	$("#courseContents table tbody").html(data.filtered_list);
				    	$("#courseContents .pagination").html(data.pagination);
				    	paginateAjax();
				    	start_tooltipster();
				    	changeWorksheet();
				    	
				    });//end .getJSON function
				    
				    //Return false if there's an issue
				    return false;
				}//endif input is unchecked
				
				//Only run this if the input that was clicked is now checked
				//Meaning we're going to show that subject now
				else if($(this).find("input").prop("checked") == true) {	
					//Store this in a variable
					var thisClickedInput = $(this).find("input");
					
					//The NONE option can only be checked if nothing is being shown
					//So if NONE was not THIS, then uncheck none
					if(thisClickedInput.attr("id") != "NONE") {
						
						//Uncheck none
						$("#dropdown-1 .dropdown-menu li input[id=NONE]").prop("checked",false);
						
						//If the clicked option wasn't all, then we're going to modify oldsubjects
						if($(this).find("input").attr("id") != "ALL") {
							//So the item isn't NONE and is a subject we now want to show
							//Now we want to check if "ALL" is already checked
							if($("#dropdown-1 .dropdown-menu li input[id=ALL]").prop("checked") == true) {
								//Empty oldsubjects, just in case
								oldsubjects = '';
								//Add all subjects (including THIS) to oldsubjects
								$('#dropdown-1 .dropdown-menu li input:checkbox').each(function(){
									oldsubjects = oldsubjects + "," + $(this).val();					
								});//endloop
								
								//Finally uncheck "ALL"
								$("#dropdown-1 .dropdown-menu li input[id=ALL]").prop("checked",false);
							}//end if "ALL" is checked
							
							//Add its value to a string surrounded by commas
							//This ensures that e.g. if we check 'CS', we replace 'CS' exactly and not 'CSYS' or something
							replaceString = "," + thisClickedInput.val() + ",";
							
							//Now replace the subject in oldsubjects with a comma
							oldsubjects = oldsubjects.replace(replaceString, ",");
						
						//Or else the clicked option was ALL, then we want to show ALL subjects, m'kay
						} else if($(this).find("input").attr("id") == "ALL") {
							//Reset oldsubjects
							oldsubjects = "";
							
							//Loop through all inputs and uncheck them
							$('#dropdown-1 .dropdown-menu li input:checkbox').each(function(){
								$(this).prop("checked",false);				
							});//end loop
							
							//And check ALL, since we're now showing all subjects
							$("#dropdown-1 .dropdown-menu li input[id=ALL]").prop("checked",true);
						}//endif (the input was "ALL")
					
					
					//Else NONE was clicked
					} else if(thisClickedInput.attr("id") == "NONE") {
						//Empty oldsubjects first
						oldsubjects = '';
						
						//Loop through all inputs, uncheck them, and add them to our filter outs
						$('#dropdown-1 .dropdown-menu li input:checkbox').each(function(){
							//Make sure we uncheck everything
							$(this).prop("checked",false);
							oldsubjects = oldsubjects + "," + $(this).val();					
						});//end loop
						
						
						//Also check none, since we just unchecked everything above
						$("#dropdown-1 .dropdown-menu li input[id=NONE]").prop("checked",true);
					}//endif
					
					
					//Send the new oldsubjects to JSON
					//And get new rendered coursecontent and .pagination
					$.getJSON($SCRIPT_ROOT + '/_course_args', {
		    			old_s: oldsubjects,
		    			old_level: oldlevels,
		    			old_day: olddays,
		    			query: getQueryVariable("q")
			    	}, 
			    	//Gets values from JSON and renders the new content
			    	function(data) {
				    	oldsubjects = data.subjects;
				    	//$('#result').text(oldsubjects)
				    	$("#courseContents table tbody").html(data.filtered_list);
				    	$("#courseContents .pagination").html(data.pagination);
				    	//We have to reload the paginate function since we're replacing the pagination html
				    	paginateAjax();
				    	start_tooltipster();
				    	changeWorksheet();
				    	
				    });//end function
				    return false;
				}//endif input is checked
			}//end if the click was not on a dropdown search
		});//end the event listener for any click on the subject dropdown
	});//end function for ALL subject filter 
	
	
	/* ++++++++++++++++++++++++++++++++++++++++++++
	 * All code for sending level filters to json
	 * ++++++++++++++++++++++++++++++++++++++++++++
	*/
	
	$(function() {
		// It all starts with a simple event listener
		// This will be *A LOT* simpler than the subjects listener(s)
		// Listen for any clicks on an li in the levels dropdown
		$('#dropdown-2 .dropdown-menu li').bind('click', function() {
			
			//Only run this is the input that was clicked is now unchecked
			//Meaning it was checked, but not anymore
			//So we're going to want to stop showing its level
			if($(this).find("input").prop("checked") == false) {
				//Send the value of the checkbox to JSON
				$.getJSON($SCRIPT_ROOT + '/_course_args', {
					new_level: $(this).find("input").val(),
					old_level: oldlevels,
					old_s: oldsubjects,
					old_day: olddays,
					query: getQueryVariable("q")
				},
				//Get values from JSON and render new content
				function(data) {
					
					oldlevels = data.levels;
					$("#courseContents table tbody").html(data.filtered_list);
					$("#courseContents .pagination").html(data.pagination);
					
					//We have to reload the paginate function since we're replacing the pagination html
					paginateAjax();
					start_tooltipster();
					changeWorksheet();
				});//end function
				return false;
			
			//Else the input is now checked
			//So we want to show that level
			} else if($(this).find("input").prop("checked") == true) {
				
				//We want to remove this level from oldlevels
				//Add its value to a string surrounded by commas
				//This is necessary for subjects, but shouldn't be necessary for levels
				//It is slightly cleaner though, since it removes trailing commas
				replaceString = "," + $(this).find("input").val() + ",";
				
				console.log(replaceString);
				//Now replace the subject in oldsubjects with a comma
				oldlevels = oldlevels.replace(replaceString, ",");
				
				//Send the new oldlevels to JSON
				//There's no new_level being sent, since we didn't uncheck anything new
				$.getJSON($SCRIPT_ROOT + '/_course_args', {
					old_level: oldlevels,
					old_s: oldsubjects,
					old_day: olddays,
					query: getQueryVariable("q")
				},
				//Get values from JSON and render new content
				function(data) {
					
					//oldlevels shouldn't changed, since data.levels is just a concatenation of old and new levels, and
					//there was no new_level in this JSON
					//Updating it just in case :)
					oldlevels = data.levels;
					
					//Update with the new page renders
					$("#courseContents table tbody").html(data.filtered_list);
					$("#courseContents .pagination").html(data.pagination);
					
					//We have to reload the paginate function since we're replacing the pagination html
					paginateAjax();
					start_tooltipster();
					changeWorksheet();
				});//end function
				return false;
			}//endif checkbox was checked
			
		});//end the event listener for any click on the levels dropdown
	});//end function
	
	
	/* ++++++++++++++++++++++++++++++++++++++++++++
	 * All code for sending day filters to json
	 * ++++++++++++++++++++++++++++++++++++++++++++
	*/
	
	$(function() {
		// It all starts with a simple event listener
		// This will be *A LOT* simpler than the subjects listener(s)
		// Listen for any clicks on an li in the days dropdown
		$('#dropdown-3 .dropdown-menu li').bind('click', function() {
			
			//Only run this is the input that was clicked is now unchecked
			//Meaning it was checked, but not anymore
			//So we're going to want to stop showing its level
			if($(this).find("input").prop("checked") == false) {
				//Send the value of the checkbox to JSON
				$.getJSON($SCRIPT_ROOT + '/_course_args', {
					new_day: $(this).find("input").val(),
					old_day: olddays,
					old_level: oldlevels,
					old_s: oldsubjects,
					query: getQueryVariable("q")
				},
				//Get values from JSON and render new content
				function(data) {
					
					olddays = data.days;
					$("#courseContents table tbody").html(data.filtered_list);
					$("#courseContents .pagination").html(data.pagination);
					
					//We have to reload the paginate function since we're replacing the pagination html
					paginateAjax();
					start_tooltipster();
					changeWorksheet();
				});//end function
				return false;
			
			//Else the input is now checked
			//So we want to show that day
			} else if($(this).find("input").prop("checked") == true) {
				
				//We want to remove this day from oldday
				//Add its value to a string surrounded by commas
				//This is necessary for subjects, but shouldn't be necessary for days
				//It is slightly cleaner though, since it removes trailing commas
				replaceString = "," + $(this).find("input").val() + ",";
				
				//console.log(replaceString);
				//Now replace the day in olddays with a comma
				olddays = olddays.replace(replaceString, ",");
				
				//Send the new olddays to JSON
				//There's no new_level being sent, since we didn't uncheck anything new
				$.getJSON($SCRIPT_ROOT + '/_course_args', {
					old_level: oldlevels,
					old_s: oldsubjects,
					old_day: olddays,
					query: getQueryVariable("q")
				},
				//Get values from JSON and render new content
				function(data) {
					
					//olddays shouldn't changed, since data.days is just a concatenation of old and new days, and
					//there was no new_day in this JSON
					//Updating it just in case :)
					olddays = data.days;
					console.log(olddays);
					//Update with the new page renders
					$("#courseContents table tbody").html(data.filtered_list);
					$("#courseContents .pagination").html(data.pagination);
					
					//We have to reload the paginate function since we're replacing the pagination html
					paginateAjax();
					start_tooltipster();
					changeWorksheet();
				});//end function
				return false;
			}//endif checkbox was checked
			
		});//end the event listener for any click on the days dropdown
	});//end function
});//end document.ready

