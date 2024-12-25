$(function() {
	"use strict";

	// chart 14
	
	async function createChart14() {
		try {
			const response = await fetch('/get_booking_total_counter');
			const data = await response.json();
			console.log("actual BOOKING TOTAL URLS", data.count)

			const response1 = await fetch('/get_booking_counter');
			const data1 = await response1.json();
			console.log("actual BOOKING now URLS", data1.count)

			if(data.count == 0 || data1.count == 0){ data.count = 1; data1.count = 0 }
	
			// If this is the first time, initialize the chart
			if (!window.myChart14) {
				var options = {
					chart: {
						height: 240,
						type: 'radialBar',
						toolbar: {
							show: false
						}
					},
					plotOptions: {
						radialBar: {
							hollow: {
								margin: 0,
								size: '80%',
								background: 'transparent',
								position: 'front',
								dropShadow: {
									enabled: false,
									top: 3,
									left: 0,
									blur: 4,
									color: 'rgba(0, 169, 255, 0.85)',
									opacity: 0.65
								}
							},
							track: {
								background: '#eee',
								strokeWidth: '67%',
								margin: 0,
								dropShadow: {
									enabled: false,
									top: -3,
									left: 0,
									blur: 4,
									color: 'rgba(0, 169, 255, 0.85)',
									opacity: 0.65
								}
							},
							dataLabels: {
								showOn: 'always',
								name: {
									offsetY: -20,
									show: true,
									color: '#212529',
									fontSize: '14px'
								},
								value: {
									formatter: function (val) {
										return val.toFixed(2) + "%";
									},
									color: '#212529',
									fontSize: '35px',
									show: true,
									offsetY: 10,
								}
							}
						}
					},
					fill: {
						type: 'gradient',
						gradient: {
							shade: 'light',
							type: 'horizontal',
							shadeIntensity: 0.5,
							gradientToColors: ['darkblue'],
							inverseColors: false,
							opacityFrom: 1,
							opacityTo: 1,
							stops: [0, 100]
						}
					},
					colors: ["blue"],
					series: [(data1.count/data.count)*100], // Assign fetched data here
					stroke: {
						lineCap: 'round',
					},
					labels: ['Booking'],
					responsive: [
						{
							breakpoint: 1281,
							options: {
								chart: {
									height: 220,
								}
							}
						}
					],
				};
	
				window.myChart14 = new ApexCharts(document.querySelector("#chart14"), options);
				window.myChart14.render();
			} else {
				// Update the existing chart with new data
				window.myChart14.updateSeries([(data1.count/data.count)*100]);
			}
		} catch (error) {
			console.error("Error fetching or updating chart data: ", error);
		}
	}
	
	// Set interval to update the chart every 500ms
	setInterval(createChart14, 4000);
	
	
	
	  
	   // chart 15
	   async function createChart15() {
		try {
			const response = await fetch('/get_airbnb_total_counter');
			const data = await response.json();
			console.log("actual AIRBNB TOTAL URLS", data.count)

			const response1 = await fetch('/get_airbnb_counter');
			const data1 = await response1.json();
			console.log("actual AIRBNB now URLS", data1.count)

			if(data.count == 0 || data1.count == 0){ data.count = 1; data1.count = 0 }
	
			// If this is the first time, initialize the chart
			if (!window.myChart) {
				var options = {
					chart: {
						height: 240,
						type: 'radialBar',
						toolbar: {
							show: false
						}
					},
					plotOptions: {
						radialBar: {
							hollow: {
								margin: 0,
								size: '80%',
								background: 'transparent',
								position: 'front',
								dropShadow: {
									enabled: false,
									top: 3,
									left: 0,
									blur: 4,
									color: 'rgba(0, 169, 255, 0.85)',
									opacity: 0.65
								}
							},
							track: {
								background: '#eee',
								strokeWidth: '67%',
								margin: 0,
								dropShadow: {
									enabled: false,
									top: -3,
									left: 0,
									blur: 4,
									color: 'rgba(0, 169, 255, 0.85)',
									opacity: 0.65
								}
							},
							dataLabels: {
								showOn: 'always',
								name: {
									offsetY: -20,
									show: true,
									color: '#212529',
									fontSize: '14px'
								},
								value: {
									formatter: function (val) {
										return val.toFixed(2) + "%";
									},
									color: '#212529',
									fontSize: '35px',
									show: true,
									offsetY: 10,
								}
							}
						}
					},
					fill: {
						type: 'gradient',
						gradient: {
							shade: 'light',
							type: 'horizontal',
							shadeIntensity: 0.5,
							gradientToColors: ['darkred'],
							inverseColors: false,
							opacityFrom: 1,
							opacityTo: 1,
							stops: [0, 100]
						}
					},
					colors: ["#ff5a5f"],
					series: [(data1.count/data.count)*100], // Assign fetched data here
					stroke: {
						lineCap: 'round',
					},
					labels: ['Airbnb'],
					responsive: [
						{
							breakpoint: 1281,
							options: {
								chart: {
									height: 220,
								}
							}
						}
					],
				};
	
				window.myChart = new ApexCharts(document.querySelector("#chart15"), options);
				window.myChart.render();
			} else {
				// Update the existing chart with new data
				window.myChart.updateSeries([(data1.count/data.count)*100]);
			}
		} catch (error) {
			console.error("Error fetching or updating chart data: ", error);
		}
	}
	
	// Set interval to update the chart every 500ms
	setInterval(createChart15, 4000);
	
	


	var options = {
		chart: {
		  height: 240,
		  type: 'radialBar',
		  toolbar: {
			show: false
		  }
		},
		plotOptions: {
		  radialBar: {
			//startAngle: -135,
			//endAngle: 225,
			 hollow: {
			  margin: 0,
			  size: '80%',
			  background: 'transparent',
			  image: undefined,
			  imageOffsetX: 0,
			  imageOffsetY: 0,
			  position: 'front',
			  dropShadow: {
				enabled: false,
				top: 3,
				left: 0,
				blur: 4,
				color: 'rgba(0, 169, 255, 0.85)',
				opacity: 0.65
			  }
			},
			track: {
			  background: '#eee',
			  strokeWidth: '67%',
			  margin: 0, // margin is in pixels
			  dropShadow: {
				enabled: false,
				top: -3,
				left: 0,
				blur: 4,
				color: 'rgba(0, 169, 255, 0.85)',
				opacity: 0.65
			  }
			},
	
			dataLabels: { 
			  showOn: 'always',
			  name: {
				offsetY: -20,
				show: true,
				color: '#212529',
				fontSize: '14px'
			  },
			  value: {
				formatter: function (val) {
						  return val + "%";
					  },
				color: '#212529',
				fontSize: '35px',
				show: true,
				offsetY: 10,
			  }
			}
		  }
		},
		fill: {
		  type: 'gradient',
		  gradient: {
			shade: 'light',
			type: 'horizontal',
			shadeIntensity: 0.5,
			gradientToColors: ['darkgreen'],
			inverseColors: false,
			opacityFrom: 1,
			opacityTo: 1,
			stops: [0, 100]
		  }
		},
		colors: ["#12bf24"],
		series: [55],
		stroke: {
		  lineCap: 'round',
		  //dashArray: 4
		},
		labels: ['Total'],
		responsive: [
			{
			  breakpoint: 1281,
			  options: {
				chart: {
					height: 220,
				}
			  }
			}
		  ],
	
	  }
	  var chart = new ApexCharts(
		document.querySelector("#chart13"),
		options
	  );
	
	  chart.render();
	

	var options = {
		chart: {
		  height: 300,
		  type: 'radialBar',
		  toolbar: {
			show: false
		  }
		},
		plotOptions: {
		  radialBar: {
			//startAngle: -135,
			//endAngle: 225,
			 hollow: {
			  margin: 0,
			  size: '80%',
			  background: 'transparent',
			  image: undefined,
			  imageOffsetX: 0,
			  imageOffsetY: 0,
			  position: 'front',
			  dropShadow: {
				enabled: true,
				top: 3,
				left: 0,
				blur: 4,
				color: 'rgba(0, 169, 255, 0.85)',
				opacity: 0.65
			  }
			},
			track: {
			  background: '#e5d1ff',
			  strokeWidth: '67%',
			  margin: 0, // margin is in pixels
			  dropShadow: {
				enabled: 0,
				top: -3,
				left: 0,
				blur: 4,
				color: 'rgba(0, 169, 255, 0.85)',
				opacity: 0.65
			  }
			},
			dataLabels: { 
			  showOn: 'always',
			  name: {
				offsetY: -20,
				show: true,
				color: '#212529',
				fontSize: '16px'
			  },
			  value: {
				formatter: function (val) {
						  return val + "%";
					  },
				color: '#212529',
				fontSize: '35px',
				show: true,
				offsetY: 10,
			  }
			}
		  }
		},
		fill: {
		  type: 'gradient',
		  gradient: {
			shade: 'light',
			type: 'horizontal',
			shadeIntensity: 0.5,
			gradientToColors: ['#8932ff'],
			inverseColors: false,
			opacityFrom: 1,
			opacityTo: 1,
			stops: [0, 100]
		  }
		},
		colors: ["#8932ff"],
		series: [78],
		stroke: {
		  lineCap: 'round',
		  //dashArray: 4
		},
		labels: ['Total Traffic'],
		responsive: [
			{
			  breakpoint: 1281,
			  options: {
				chart: {
					height: 280,
				}
			  }
			}
		  ],
	
	  }
	
	  var chart = new ApexCharts(
		document.querySelector("#chart7"),
		options
	  );
	
	  chart.render();

// total des annonces
async function fetchTotalAnnData() {
    try {
        const response = await fetch('/get_monthly_total_counts');
        const data = await response.json();

		document.querySelector("#total_annonces").innerHTML = data.total
		
	}
	catch (error) {
        console.error('Error fetching total des annonces:', error);
    }
}
fetchTotalAnnData()


// Airnbnb counter

async function fetch_airbnb_counter() {
    try {
        const response = await fetch('/get_airbnb_real_time_counter');
        const data = await response.json();

		document.querySelector("#airbnb").innerHTML = data.count
		
	}
	catch (error) {
        console.error('Error fetching total des annonces:', error);
    }
}
setInterval(fetch_airbnb_counter, 4000)


// Booking counter

async function fetch_booking_counter() {
    try {
        const response = await fetch('/get_booking_real_time_counter');
        const data = await response.json();

		document.querySelector("#booking").innerHTML = data.count
		
	}
	catch (error) {
        console.error('Error fetching total des annonces:', error);
    }
}
setInterval(fetch_booking_counter, 4000)

//setInterval(fetchTotalAnnData, 4000)

// test
async function get_weekly_total_counts() {
    try {
        const response = await fetch('/get_weekly_total_counts');
        const data = await response.json();
		console.log(data.booking_scraped_urls.data);
		console.log(data.airbnb_scraped_urls.data);
		document.querySelector(".txt").innerHTML = data.booking_scraped_urls.total
		document.querySelector(".txt2").innerHTML = data.airbnb_scraped_urls.total
		
		var options = {
			series: [{
				name: "Airbnb",
				data: data.airbnb_scraped_urls.data
			},{
				name: "Booking",
				data: data.booking_scraped_urls.data
			}],
			chart: {
				foreColor: '#9a9797',
				type: "bar",
				width: "75%",
				stacked: true,
				height: 280,
				toolbar: {
					show: !1
				},
				zoom: {
					enabled: !1
				},
				dropShadow: {
					enabled: 0,
					top: 3,
					left: 15,
					blur: 4,
					opacity: .12,
					color: "#3461ff"
				},
				sparkline: {
					enabled: !1
				}
			},
			markers: {
				size: 0,
				colors: ["#3461ff", "#c1cfff"],
				strokeColors: "#fff",
				strokeWidth: 2,
				hover: {
					size: 7
				}
			},
			plotOptions: {
				bar: {
					horizontal: !1,
					columnWidth: "35%",
					//endingShape: "rounded"
				}
			},
			dataLabels: {
				enabled: !1
			},
			legend: {
				show: true,
			},
			stroke: {
				show: !0,
				width: 0,
				curve: "smooth"
			},
			colors: ["#ff5a5f", "#23387e"],
			xaxis: {
				categories: ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
			},
			grid:{
				show: true,
				borderColor: 'rgba(66, 59, 116, 0.15)',
			},
			tooltip: {
				theme: "dark",
				fixed: {
					enabled: !1
				},
				x: {
					show: !1
				},
				y: {
					title: {
						formatter: function(e) {
							return ""
						}
					}
				},
				marker: {
					show: !1
				}
			}
		  };
		
		  var chart = new ApexCharts(document.querySelector("#chart11"), options);
		  chart.render();
				
	}
	catch (error) {
        console.error('Error fetching total des annonces:', error);
    }
}
get_weekly_total_counts()

// Aujourd'hui

async function fetchTodayAnnData() {
    try {
        const response = await fetch('/get_today_counts');
        const data = await response.json();
		
		document.querySelector("#today").innerHTML = data.total
		
	}
	catch (error) {
        console.error('Error fetching total des annonces pour aujourd\'hui:', error);
    }
}
fetchTodayAnnData()
//setInterval(fetchTodayAnnData, 4000)
// chart 1

var options = {
	series: [{
		name: "Total Orders",
		data: [240, 160, 671, 414, 555, 257, 240, 160, 671, 414, 555, 257]
	}],
	chart: {
		type: "line",
		//width: 100%,
		height: 40,
		toolbar: {
			show: !1
		},
		zoom: {
			enabled: !1
		},
		dropShadow: {
			enabled: 0,
			top: 3,
			left: 14,
			blur: 4,
			opacity: .12,
			color: "#e72e7a"
		},
		sparkline: {
			enabled: !0
		}
	},
	markers: {
		size: 0,
		colors: ["#e72e7a"],
		strokeColors: "#fff",
		strokeWidth: 2,
		hover: {
			size: 7
		}
	},
	plotOptions: {
		bar: {
			horizontal: !1,
			columnWidth: "35%",
			endingShape: "rounded"
		}
	},
	dataLabels: {
		enabled: !1
	},
	stroke: {
		show: !0,
		width: 2.5,
		curve: "smooth"
	},
	colors: ["#e72e7a"],
	xaxis: {
		categories: ["Jan", "Fev", "Mar", "Avr", "Mai", "Jui", "Jul", "Aou", "Sep", "Oct", "Nov", "Dec"]
	},
	fill: {
		opacity: 1
	},
	tooltip: {
		theme: "dark",
		fixed: {
			enabled: !1
		},
		x: {
			show: !1
		},
		y: {
			title: {
				formatter: function(e) {
					return ""
				}
			}
		},
		marker: {
			show: !1
		}
	}
  };

  var chart = new ApexCharts(document.querySelector("#chart1"), options);
  chart.render();

// chart 2
var options = {
	series: [{
		name: "Total Views",
		data: [400, 555, 257, 640, 460, 671, 350]
	}],
	chart: {
		type: "bar",
		//width: 100%,
		height: 40,
		toolbar: {
			show: !1
		},
		zoom: {
			enabled: !1
		},
		dropShadow: {
			enabled: 0,
			top: 3,
			left: 14,
			blur: 4,
			opacity: .12,
			color: "#ffffff"
		},
		sparkline: {
			enabled: !0
		}
	},
	markers: {
		size: 0,
		colors: ["#ffffff"],
		strokeColors: "#fff",
		strokeWidth: 2,
		hover: {
			size: 7
		}
	},
	plotOptions: {
		bar: {
			horizontal: !1,
			columnWidth: "35%",
			endingShape: "rounded"
		}
	},
	dataLabels: {
		enabled: !1
	},
	stroke: {
		show: !0,
		width: 2.5,
		curve: "smooth"
	},
	colors: ["#ffffff"],
	xaxis: {
		categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
	},
	fill: {
		opacity: 1
	},
	tooltip: {
		theme: "dark",
		fixed: {
			enabled: !1
		},
		x: {
			show: !1
		},
		y: {
			title: {
				formatter: function(e) {
					return ""
				}
			}
		},
		marker: {
			show: !1
		}
	}
  };

  var charts = document.querySelectorAll("#chart2");
  charts.forEach(chart => {
	chart = new ApexCharts(chart, options)
	chart.render();
  });



// chart 3
var options = {
	series: [{
		name: "Revenue",
		data: [240, 160, 555, 257, 671, 414]
	}],
	chart: {
		type: "line",
		//width: 100%,
		height: 40,
		toolbar: {
			show: !1
		},
		zoom: {
			enabled: !1
		},
		dropShadow: {
			enabled: 0,
			top: 3,
			left: 14,
			blur: 4,
			opacity: .12,
			color: "#12bf24"
		},
		sparkline: {
			enabled: !0
		}
	},
	markers: {
		size: 0,
		colors: ["#12bf24"],
		strokeColors: "#fff",
		strokeWidth: 2,
		hover: {
			size: 7
		}
	},
	plotOptions: {
		bar: {
			horizontal: !1,
			columnWidth: "35%",
			endingShape: "rounded"
		}
	},
	dataLabels: {
		enabled: !1
	},
	stroke: {
		show: !0,
		width: 2.5,
		curve: "smooth"
	},
	colors: ["#12bf24"],
	xaxis: {
		categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
	},
	fill: {
		opacity: 1
	},
	tooltip: {
		theme: "dark",
		fixed: {
			enabled: !1
		},
		x: {
			show: !1
		},
		y: {
			title: {
				formatter: function(e) {
					return ""
				}
			}
		},
		marker: {
			show: !1
		}
	}
  };

  var chart = new ApexCharts(document.querySelector("#chart3"), options);
  chart.render();




// chart 4
const active = true;
var options = {
	series: [{
		name: "stop",
		data: !active ? [1,1,1,1,1,1,1] : [0,0,0,0,0,0,0]
	}],
	chart: {
		type: "bar",
		//width: 100%,
		height: 30,
		toolbar: {
			show: !1
		},
		zoom: {
			enabled: !1
		},
		dropShadow: {
			enabled: 0,
			top: 3,
			left: 14,
			blur: 4,
			opacity: .12,
			color: "#ff6632"
		},
		sparkline: {
			enabled: !0
		}
	},
	markers: {
		size: 0,
		colors: ["#ff6632"],
		strokeColors: "#fff",
		strokeWidth: 2,
		hover: {
			size: 7
		}
	},
	plotOptions: {
		bar: {
			horizontal: !1,
			columnWidth: "35%",
			endingShape: "rounded"
		}
	},
	dataLabels: {
		enabled: !1
	},
	stroke: {
		show: !0,
		width: 2.5,
		curve: "smooth"
	},
	colors: ["#ffffff"],
	xaxis: {
		categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
	},
	fill: {
		opacity: 1
	},
	tooltip: {
		enabled: false,
		theme: "dark",
		fixed: {
			enabled: !1
		},
		x: {
			show: !1
		},
		y: {
			title: {
				formatter: function(e) {
					return ""
				}
			}
		},
		marker: {
			show: !1
		}
	}
  };

  var charts = document.querySelectorAll("#chart4");
  charts.forEach(chart => {
	chart = new ApexCharts(chart, options)
	chart.render();
  });



// chart 5
let chart5; 

async function fetchChartData() { 
    try {
        const response = await fetch('/get_chart5_data');
        const data = await response.json();
        
        if (chart5) {
            chart5.updateSeries([{
                name: "Total announcements",
                data: data.data
            }]);
        } else {
            // Initialize the chart only once
            const options = {
                series: [{
                    name: "Total announcements",
                    data: data.data
                }],
                chart: {
                    type: "bar",
                    stacked: true,
                    height: 280,
                    toolbar: {
                        show: false
                    },
                    zoom: {
                        enabled: false
                    },
                    dropShadow: {
                        enabled: false,
                        top: 3,
                        left: 14,
                        blur: 4,
                        opacity: 0.12,
                        color: "#3461ff"
                    },
                    sparkline: {
                        enabled: false
                    }
                },
                markers: {
                    size: 0,
                    colors: ["#3461ff"],
                    strokeColors: "#fff",
                    strokeWidth: 2,
                    hover: {
                        size: 7
                    }
                },
                plotOptions: {
                    bar: {
                        horizontal: false,
                        columnWidth: "35%",
                        endingShape: "rounded"
                    }
                },
                dataLabels: {
                    enabled: false
                },
                stroke: {
                    show: true,
                    width: 2.5,
                    curve: "smooth"
                },
                colors: ["#3461ff"],
                xaxis: {
                    categories: ["Jan", "Fev", "Mar", "Avr", "Mai", "Jun", "Jul", "Aou", "Sep", "Oct", "Nov", "Dec"]
                },
                fill: {
                    opacity: 1
                },
                tooltip: {
                    theme: "dark",
                    fixed: {
                        enabled: false
                    },
                    x: {
                        show: false
                    },
                    y: {
                        title: {
                            formatter: function() {
                                return "";
                            }
                        }
                    },
                    marker: {
                        show: false
                    }
                }
            };

            // Create and render the chart
            chart5 = new ApexCharts(document.querySelector("#chart5"), options);
            chart5.render();
        }
    } catch (error) {
        console.error('Error fetching chart data:', error);
    }
}

fetchChartData()
//setInterval(fetchChartData, 4000)


// chart6
async function fetchTotalAnnAirbnb() {
	try {
        const response = await fetch('/get_monthly_total_counts');
        const data = await response.json();
		var chart = new Chart(document.getElementById('chart6'), {
			type: 'doughnut',
			data: {
				labels: ["Airbnb", "Booking"],
				datasets: [{
					label: "Device Users",
					backgroundColor: ["#ff5a5f", "#23387e", "#ff6632"],
					data: [data.data.airbnb_scraped_urls, data.data.booking_scraped_urls]
				}]
			},
			options: {
				maintainAspectRatio: false,
				cutoutPercentage: 45,
				responsive: true,
			legend: {
				display: false
			}
			}
		});
	} catch (error) {
        console.error('Error fetching airbnb data:', error);
    }
}
fetchTotalAnnAirbnb();




  
   // chart 7

   var options = {
	chart: {
	  height: 300,
	  type: 'radialBar',
	  toolbar: {
		show: false
	  }
	},
	plotOptions: {
	  radialBar: {
		//startAngle: -135,
		//endAngle: 225,
		 hollow: {
		  margin: 0,
		  size: '80%',
		  background: 'transparent',
		  image: undefined,
		  imageOffsetX: 0,
		  imageOffsetY: 0,
		  position: 'front',
		  dropShadow: {
			enabled: true,
			top: 3,
			left: 0,
			blur: 4,
			color: 'rgba(0, 169, 255, 0.85)',
			opacity: 0.65
		  }
		},
		track: {
		  background: '#e5d1ff',
		  strokeWidth: '67%',
		  margin: 0, // margin is in pixels
		  dropShadow: {
			enabled: 0,
			top: -3,
			left: 0,
			blur: 4,
			color: 'rgba(0, 169, 255, 0.85)',
			opacity: 0.65
		  }
		},
		dataLabels: { 
		  showOn: 'always',
		  name: {
			offsetY: -20,
			show: true,
			color: '#212529',
			fontSize: '16px'
		  },
		  value: {
			formatter: function (val) {
					  return val + "%";
				  },
			color: '#212529',
			fontSize: '35px',
			show: true,
			offsetY: 10,
		  }
		}
	  }
	},
	fill: {
	  type: 'gradient',
	  gradient: {
		shade: 'light',
		type: 'horizontal',
		shadeIntensity: 0.5,
		gradientToColors: ['#8932ff'],
		inverseColors: false,
		opacityFrom: 1,
		opacityTo: 1,
		stops: [0, 100]
	  }
	},
	colors: ["#8932ff"],
	series: [78],
	stroke: {
	  lineCap: 'round',
	  //dashArray: 4
	},
	labels: ['Total Traffic'],
	responsive: [
		{
		  breakpoint: 1281,
		  options: {
			chart: {
				height: 280,
			}
		  }
		}
	  ],

  }

  var chart = new ApexCharts(
	document.querySelector("#chart7"),
	options
  );

  chart.render();


   
// chart 8

var options = {
    series: [{
        name: "Messages",
        data: [0, 160, 671, 414, 555, 257, 901, 613, 727, 414, 555, 0]
    }],
    chart: {
        type: "area",
        //width: 130,
        height: 55,
        toolbar: {
            show: !1
        },
        zoom: {
            enabled: !1
        },
        dropShadow: {
            enabled: 0,
            top: 3,
            left: 14,
            blur: 4,
            opacity: .12,
            color: "#e72e2e"
        },
        sparkline: {
            enabled: !0
        }
    },
    markers: {
        size: 0,
        colors: ["#e72e7a"],
        strokeColors: "#fff",
        strokeWidth: 2,
        hover: {
            size: 7
        }
    },
    plotOptions: {
        bar: {
            horizontal: !1,
            columnWidth: "35%",
            endingShape: "rounded"
        }
    },
    dataLabels: {
        enabled: !1
    },
    stroke: {
        show: !0,
        width: 2.5,
        curve: "smooth"
    },
	fill: {
		type: 'gradient',
		gradient: {
		  shade: 'light',
		  type: 'vertical',
		  shadeIntensity: 0.5,
		  gradientToColors: ['#e72e7a'],
		  inverseColors: false,
		  opacityFrom: 0.6,
		  opacityTo: 0.1,
		  //stops: [0, 100]
		}
	  },
    colors: ["#e72e7a"],
    xaxis: {
        categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    },
	grid:{
		show: false,
		borderColor: 'rgba(66, 59, 116, 0.15)',
	},
    tooltip: {
        theme: "dark",
        fixed: {
            enabled: !1
        },
        x: {
            show: !1
        },
        y: {
            title: {
                formatter: function(e) {
                    return ""
                }
            }
        },
        marker: {
            show: !1
        }
    }
  };

  var chart = new ApexCharts(document.querySelector("#chart8"), options);
  chart.render();


   
// chart 9

var options = {
    series: [{
        name: "Posts",
        data: [0, 160, 671, 414, 555, 257, 901, 613, 727, 414, 555, 0]
    }],
    chart: {
        type: "area",
        //width: 130,
        height: 55,
        toolbar: {
            show: !1
        },
        zoom: {
            enabled: !1
        },
        dropShadow: {
            enabled: 0,
            top: 3,
            left: 14,
            blur: 4,
            opacity: .12,
            color: "#12bf24"
        },
        sparkline: {
            enabled: !0
        }
    },
    markers: {
        size: 0,
        colors: ["#3461ff"],
        strokeColors: "#fff",
        strokeWidth: 2,
        hover: {
            size: 7
        }
    },
    plotOptions: {
        bar: {
            horizontal: !1,
            columnWidth: "35%",
            endingShape: "rounded"
        }
    },
    dataLabels: {
        enabled: !1
    },
    stroke: {
        show: !0,
        width: 2.5,
        curve: "smooth"
    },
    fill: {
		type: 'gradient',
		gradient: {
		  shade: 'light',
		  type: 'vertical',
		  shadeIntensity: 0.5,
		  gradientToColors: ['#12bf24'],
		  inverseColors: false,
		  opacityFrom: 0.6,
		  opacityTo: 0.1,
		  //stops: [0, 100]
		}
	  },
    colors: ["#12bf24"],
    xaxis: {
        categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    },
    tooltip: {
        theme: "dark",
        fixed: {
            enabled: !1
        },
        x: {
            show: !1
        },
        y: {
            title: {
                formatter: function(e) {
                    return ""
                }
            }
        },
        marker: {
            show: !1
        }
    }
  };

  var chart = new ApexCharts(document.querySelector("#chart9"), options);
  chart.render();



   
// chart 10

var options = {
    series: [{
        name: "Tasks",
        data: [0, 160, 671, 414, 555, 257, 901, 613, 727, 414, 555, 0]
    }],
    chart: {
        type: "area",
        //width: 130,
        height: 55,
        toolbar: {
            show: !1
        },
        zoom: {
            enabled: !1
        },
        dropShadow: {
            enabled: 0,
            top: 3,
            left: 14,
            blur: 4,
            opacity: .12,
            color: "#32bfff"
        },
        sparkline: {
            enabled: !0
        }
    },
    markers: {
        size: 0,
        colors: ["#32bfff"],
        strokeColors: "#fff",
        strokeWidth: 2,
        hover: {
            size: 7
        }
    },
    plotOptions: {
        bar: {
            horizontal: !1,
            columnWidth: "35%",
            endingShape: "rounded"
        }
    },
    dataLabels: {
        enabled: !1
    },
    stroke: {
        show: !0,
        width: 2.5,
        curve: "smooth"
    },
    fill: {
		type: 'gradient',
		gradient: {
		  shade: 'light',
		  type: 'vertical',
		  shadeIntensity: 0.5,
		  gradientToColors: ['#32bfff'],
		  inverseColors: false,
		  opacityFrom: 0.6,
		  opacityTo: 0.1,
		  //stops: [0, 100]
		}
	  },
    colors: ["#32bfff"],
    xaxis: {
        categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    },
    tooltip: {
        theme: "dark",
        fixed: {
            enabled: !1
        },
        x: {
            show: !1
        },
        y: {
            title: {
                formatter: function(e) {
                    return ""
                }
            }
        },
        marker: {
            show: !1
        }
    }
  };




// worls map

jQuery('#geographic-map').vectorMap(
	{
		map: 'uk_mill_en',
		backgroundColor: 'transparent',
		borderColor: '#818181',
		borderOpacity: 0.25,
		borderWidth: 1,
		zoomOnScroll: false,
		color: '#009efb',
		regionStyle : {
			initial : {
			  fill : '#3461ff'
			}
		  },
		markerStyle: {
		  initial: {
					r: 9,
					'fill': '#fff',
					'fill-opacity':1,
					'stroke': '#000',
					'stroke-width' : 5,
					'stroke-opacity': 0.4
					},
					},
		enableZoom: true,
		hoverColor: '#009efb',
		markers : [{
			latLng : [21.00, 78.00],
			name : 'Lorem Ipsum Dollar'
		  
		  }],
		hoverOpacity: null,
		normalizeFunction: 'linear',
		scaleColors: ['#b6d6ff', '#005ace'],
		selectedColor: '#c9dfaf',
		selectedRegions: [],
		showTooltip: true,
	});





    
});