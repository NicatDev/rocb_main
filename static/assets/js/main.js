/***************************************************
==================== JS INDEX ======================
****************************************************
Preloader js
Data js
Sticky Nav Js
Mobile Menu Js
Search Bar Js
Rating Js
Client-slider Js
Marquee slider Js
Project Slider Js
Project Slider 2 Js
Testimonial Slider Js
Testimonial Slider 2 Js
Testimonial Slider 3 Js
Hero slider Js
Service Slider Js
Blog Slider Js
Accordion Js
Project Hover active
Backtotop Js
Odometer js
VenoBox Js
Progressbar js

****************************************************/

(function ($) {
	"use strict";

	// Preloader js
	$(window).on("load", function () {
		const tjPreloader = $(".tj-preloader");
		if (tjPreloader?.length) {
			setTimeout(function () {
				tjPreloader.removeClass("is-loading").addClass("is-loaded");
				setTimeout(function () {
					tjPreloader.fadeOut(400);
					wowController();
					gsapController();
				}, 700);
			}, 2000);
		} else {
			wowController();
			gsapController();
		}
	});

	////////////////////////////////////////////////////
	// Data js
	$("[data-bg-image]").each(function () {
		var $this = $(this),
			$image = $this.data("bg-image");
		$this.css("background-image", "url(" + $image + ")");
	});

	////////////////////////////////////////////////////
	// Sticky Nav Js
	var lastScrollTop = "";
	function stickyMenu($targetMenu, $toggleClass) {
		var st = $(window).scrollTop();
		if ($(window).scrollTop() > 500) {
			if (st > lastScrollTop) {
				$targetMenu.removeClass($toggleClass);
			} else {
				$targetMenu.addClass($toggleClass);
			}
		} else {
			$targetMenu.removeClass($toggleClass);
		}

		lastScrollTop = st;
	}

	$(window).on("scroll", function () {
		if ($(".header-area").length) {
			stickyMenu($(".header-sticky"), "sticky");
		}
	});

	////////////////////////////////////////////////////
	// Mobile Menu Js
	$(".mobile_menu_bar").on("click", function () {
		$(this).toggleClass("on");
	});

	// Mobile Menu Js
	$("#mobile-menu").meanmenu({
		meanMenuContainer: ".mobile_menu",
		meanScreenWidth: "991",
		meanExpand: ['<i class="tji-arrow-down"></i>'],
	});

	// Hamburger Menu Js
	$(".mobile_menu_bar").on("click", function () {
		$(".hamburger-area").addClass("opened");
		$(".body-overlay").addClass("opened");
		$("body").toggleClass("overflow-hidden");
	});

	// Offcanvas js
	$(".menu_offcanvas").on("click", function () {
		$(".tj-offcanvas-area").toggleClass("opened");
		$(".body-overlay").addClass("opened");
		$("body").toggleClass("overflow-hidden");
	});
	$(".hamburger_close_btn").on("click", function () {
		$(".tj-offcanvas-area").removeClass("opened");
		$(".hamburger-area").removeClass("opened");
		$(".body-overlay").removeClass("opened");
		$("body").toggleClass("overflow-hidden");
	});
	$(".body-overlay").on("click", function () {
		$(".tj-offcanvas-area").removeClass("opened");
		$(".hamburger-area").removeClass("opened");
		$(".body-overlay").removeClass("opened");
		$("body").toggleClass("overflow-hidden");
	});

	////////////////////////////////////////////////////
	// Search Bar Js
	$(".header-search .search").on("click", function () {
		$(this).addClass("search-hide");
		$(".search_close_btn").addClass("close-show");
		$(".search_popup").addClass("search-opened");
		$(".search-popup-overlay").addClass("search-popup-overlay-open");
	});
	$(".search_close_btn, .search-popup-overlay").on("click", function () {
		$(".header-search .search").removeClass("search-hide");
		$(".search_popup").removeClass("search-opened");
		$(".search-popup-overlay").removeClass("search-popup-overlay-open");
		$(".search_close_btn").removeClass("close-show");
	});

	////////////////////////////////////////////////////
	// Rating Js
	if ($(".fill-ratings span").length > 0) {
		var star_rating_width = $(".fill-ratings span").width();
		$(".star-ratings").width(star_rating_width);
	}

	////////////////////////////////////////////////////
	// Nice Select Js
	if ($("select").length > 0) {
		$("select").niceSelect();
	}

	////////////////////////////////////////////////////
	// Client-slider Js
	if ($(".client-slider").length > 0) {
		var client = new Swiper(".client-slider", {
			slidesPerView: "auto",
			spaceBetween: 0,
			freemode: true,
			centeredSlides: true,
			loop: true,
			speed: 5000,
			allowTouchMove: false,
			autoplay: {
				delay: 1,
				disableOnInteraction: true,
			},
		});
	}

	////////////////////////////////////////////////////
	// Marquee slider Js
	if ($(".marquee-slider").length > 0) {
		var marquee = new Swiper(".marquee-slider", {
			slidesPerView: "auto",
			spaceBetween: 0,
			freemode: true,
			centeredSlides: true,
			loop: true,
			speed: 7000,
			allowTouchMove: false,
			autoplay: {
				delay: 1,
				disableOnInteraction: true,
			},
		});
	}
	if ($(".h7-team-marquee").length > 0) {
		var marquee = new Swiper(".h7-team-marquee", {
			slidesPerView: "auto",
			spaceBetween: 10,
			freemode: true,
			centeredSlides: true,
			loop: true,
			speed: 7000,
			allowTouchMove: false,
			autoplay: {
				delay: 1,
				disableOnInteraction: true,
			},
			breakpoints: {
				992: {
					spaceBetween: 15,
				},
			},
		});
	}

	////////////////////////////////////////////////////
	// Project Slider Js
	if ($(".project-slider").length > 0) {
		var work = new Swiper(".project-slider", {
			slidesPerView: 3,
			spaceBetween: 30,
			centeredSlides: true,
			loop: true,
			autoplay: {
				delay: 6000,
			},
			speed: 1500,
			pagination: {
				el: ".swiper-pagination-area",
				clickable: true,
			},
			breakpoints: {
				0: {
					slidesPerView: 1.2,
					spaceBetween: 15,
				},
				576: {
					slidesPerView: 1.7,
					spaceBetween: 20,
				},
				768: {
					slidesPerView: 2,
					spaceBetween: 20,
				},
				992: {
					slidesPerView: 2,
				},
				1024: {
					slidesPerView: 2.2,
				},
				1400: {
					slidesPerView: 2.31,
				},
			},
		});
	}

	// Project Slider 2 Js
	if ($(".project-slider-2").length > 0) {
		var work = new Swiper(".project-slider-2", {
			slidesPerView: 4,
			spaceBetween: 30,
			loop: true,
			speed: 1500,
			navigation: {
				nextEl: ".slider-next",
				prevEl: ".slider-prev",
			},
			pagination: {
				el: ".swiper-pagination-area",
				clickable: true,
			},
			breakpoints: {
				0: {
					slidesPerView: 1.2,
					spaceBetween: 15,
				},
				580: {
					slidesPerView: 2,
					spaceBetween: 20,
				},
				992: {
					slidesPerView: 3,
					spaceBetween: 20,
				},
				1500: {
					slidesPerView: 4,
					spaceBetween: 30,
				},
			},
		});
	}

	// Project Slider 3 Js
	if ($(".project-slider-3").length > 0) {
		var work = new Swiper(".project-slider-3", {
			slidesPerView: 3,
			spaceBetween: 30,
			centeredSlides: false,
			loop: true,
			autoplay: {
				delay: 6000,
			},
			speed: 1500,
			pagination: {
				el: ".swiper-pagination-area",
				clickable: true,
			},
			breakpoints: {
				0: {
					slidesPerView: 1.2,
					spaceBetween: 15,
				},
				576: {
					slidesPerView: 1.5,
					spaceBetween: 20,
				},
				768: {
					slidesPerView: 2,
					spaceBetween: 20,
				},
				992: {
					slidesPerView: 2.4,
				},
				1200: {
					slidesPerView: 3,
				},
			},
		});
	}

	////////////////////////////////////////////////////
	// Testimonial Slider Js
	if ($(".testimonial-slider").length > 0) {
		var testimonial = new Swiper(".testimonial-slider", {
			slidesPerView: 3,
			spaceBetween: 28,
			centeredSlides: true,
			loop: true,
			speed: 1500,
			autoplay: {
				delay: 3000,
			},
			navigation: {
				nextEl: ".slider-next",
				prevEl: ".slider-prev",
			},
			pagination: {
				el: ".swiper-pagination-area",
				clickable: true,
			},
			breakpoints: {
				0: {
					slidesPerView: 1.2,
					spaceBetween: 15,
					centeredSlides: false,
				},
				576: {
					slidesPerView: 1.3,
					spaceBetween: 20,
					centeredSlides: false,
				},
				768: {
					slidesPerView: 1.4,
					spaceBetween: 20,
					centeredSlides: false,
				},
				992: {
					slidesPerView: 3,
				},
				1200: {
					slidesPerView: 3,
				},
			},
		});
	}

	// Testimonial Slider 2 Js
	if ($(".testimonial-slider-2").length > 0) {
		var testimonial = new Swiper(".testimonial-slider-2", {
			slidesPerView: 1,
			spaceBetween: 28,
			loop: true,
			speed: 1500,
			autoplay: {
				delay: 3000,
			},
			navigation: {
				nextEl: ".slider-next",
				prevEl: ".slider-prev",
			},
			pagination: {
				el: ".swiper-pagination-area",
				clickable: true,
			},
		});
	}
	let verticalTestimonialSlider8;
	//  testimonial Slider  Js
	function verticalTestimonialSlider() {
		const screenWidth = window.innerWidth;
		const direction = screenWidth >= 992 ? "vertical" : "horizontal";
		if (verticalTestimonialSlider8) {
			verticalTestimonialSlider8?.destroy(true, true);
		}
		if ($(".h6-testimonial-slider").length > 0) {
			verticalTestimonialSlider8 = new Swiper(".h6-testimonial-slider", {
				direction: direction,
				slidesPerView: 1,
				spaceBetween: 20,
				loop: true,
				speed: 1000,
				autoplay: {
					delay: 5000,
				},

				breakpoints: {
					576: {
						slidesPerView: 1.2,
					},
					992: {
						slidesPerView: "auto",
						spaceBetween: 30,
					},
				},
			});
		}
	}
	verticalTestimonialSlider();
	// Reinitialize on resize
	window.addEventListener("resize", () => {
		verticalTestimonialSlider();
	});

	// Testimonial Slider 3 Js
	if ($(".client-thumb").length > 0 && $(".testimonial-slider-3").length > 0) {
		let thumbSlider3 = new Swiper(".client-thumb", {
			slidesPerView: 3,
			spaceBetween: 12,
			loop: true,
			speed: 1500,
			centeredSlides: true,
			freeMode: true,
			watchSlidesProgress: true,
			slideToClickedSlide: true,
		});

		let testimonialSlider3 = new Swiper(".testimonial-slider-3", {
			slidesPerView: "auto",
			spaceBetween: 28,
			loop: true,
			speed: 1500,
			autoplay: {
				delay: 3000,
			},
			navigation: {
				nextEl: ".slider-next",
				prevEl: ".slider-prev",
			},
			pagination: {
				el: ".swiper-pagination-area",
				clickable: true,
			},
		});

		// Connect the sliders
		testimonialSlider3.controller.control = thumbSlider3;
		thumbSlider3.controller.control = testimonialSlider3;
	}

	// Testimonial 5 Slider Js
	if ($(".h5-testimonial-slider").length > 0) {
		var swiper = new Swiper(".h5-testimonial-slider", {
			slidesPerView: 1.2,
			spaceBetween: 20,
			centeredSlides: true,
			loop: true,
			speed: 1500,
			pagination: {
				el: ".swiper-pagination-area",
				clickable: true,
			},
			autoplay: {
				delay: 7000,
				disableOnInteraction: true,
			},

			breakpoints: {
				992: {
					centeredSlides: false,
					slidesPerView: 2,
					spaceBetween: 30,
				},
			},
		});
	}

	////////////////////////////////////////////////////
	// Hero slider Js
	if ($(".hero-thumb").length > 0) {
		var swiper = new Swiper(".hero-thumb", {
			loop: false,
			spaceBetween: 15,
			slidesPerView: 3,
			freeMode: true,
			watchSlidesProgress: true,
		});
	}
	if ($(".hero-slider").length > 0) {
		var hero = new Swiper(".hero-slider", {
			slidesPerView: 1,
			spaceBetween: 0,
			effect: "fade",
			loop: true,
			speed: 1400,
			autoplay: {
				delay: 5000,
			},
			navigation: {
				nextEl: ".slider-next",
				prevEl: ".slider-prev",
			},
			thumbs: {
				swiper: swiper,
			},
		});
	}
	if ($(".h6-hero-card-slider").length > 0) {
		var heroCard = new Swiper(".h6-hero-card-slider", {
			slidesPerView: 1,
			spaceBetween: 15,

			loop: true,
			speed: 1400,
			autoplay: {
				delay: 5000,
			},
			pagination: {
				el: ".swiper-pagination-area",
				clickable: true,
			},
		});
	}

	////////////////////////////////////////////////////
	// Service Slider Js
	if ($(".service-slider").length > 0) {
		var service = new Swiper(".service-slider", {
			slidesPerView: 4.2,
			spaceBetween: 28,
			centeredSlides: true,
			loop: true,
			speed: 1500,
			autoplay: {
				delay: 2000,
			},
			navigation: {
				nextEl: ".slider-next",
				prevEl: ".slider-prev",
			},
			pagination: {
				el: ".swiper-pagination-area",
				clickable: true,
			},
			breakpoints: {
				0: {
					slidesPerView: 1.3,
					spaceBetween: 15,
				},
				576: {
					slidesPerView: 2,
					spaceBetween: 15,
				},
				768: {
					slidesPerView: 2.3,
					spaceBetween: 15,
				},
				900: {
					slidesPerView: 2.6,
					spaceBetween: 15,
				},
				1024: {
					slidesPerView: 3.2,
					spaceBetween: 15,
				},
				1200: {
					slidesPerView: 3.4,
					spaceBetween: 28,
				},
				1400: {
					slidesPerView: 4.2,
				},
			},
		});
	}

	// Service Slider 2 Js
	if ($(".service-slider-2").length > 0) {
		var service = new Swiper(".service-slider-2", {
			slidesPerView: 4,
			spaceBetween: 28,
			centeredSlides: false,
			loop: true,
			speed: 1500,
			autoplay: {
				delay: 2000,
				disableOnInteraction: true,
			},
			navigation: {
				nextEl: ".slider-next",
				prevEl: ".slider-prev",
			},
			pagination: {
				el: ".swiper-pagination-area",
				clickable: true,
			},
			breakpoints: {
				0: {
					slidesPerView: 1.3,
					spaceBetween: 15,
				},
				576: {
					slidesPerView: 2,
					spaceBetween: 15,
				},
				992: {
					slidesPerView: 3,
					spaceBetween: 15,
				},
				1200: {
					slidesPerView: 4,
					spaceBetween: 20,
				},
				1400: {
					slidesPerView: 4,
					spaceBetween: 28,
				},
			},
		});
	}

	// Service Slider 6 Js
	if ($(".h6-service-slider").length > 0) {
		var service = new Swiper(".h6-service-slider", {
			slidesPerView: 1,
			spaceBetween: 15,
			loop: true,
			speed: 1500,
			autoplay: {
				delay: 2000,
			},
			pagination: {
				el: ".swiper-pagination-area",
				clickable: true,
			},
			breakpoints: {
				768: {
					slidesPerView: 2,
					spaceBetween: 30,
				},
				1200: {
					slidesPerView: 3,
					spaceBetween: 30,
				},
			},
		});
	}

	////////////////////////////////////////////////////
	// Blog Slider Js
	if ($(".blog-slider").length > 0) {
		var blog = new Swiper(".blog-slider", {
			slidesPerView: 2,
			spaceBetween: 30,
			loop: true,
			speed: 1500,
			autoplay: {
				delay: 2000,
			},
			navigation: {
				nextEl: ".slider-next",
				prevEl: ".slider-prev",
			},
			pagination: {
				el: ".swiper-pagination-area",
				clickable: true,
			},
			breakpoints: {
				0: {
					slidesPerView: 1,
					spaceBetween: 15,
				},
				576: {
					slidesPerView: 1,
					spaceBetween: 15,
				},
				768: {
					slidesPerView: 1,
					spaceBetween: 20,
				},
				992: {
					slidesPerView: 2,
					spaceBetween: 20,
				},
				1200: {
					slidesPerView: 2,
				},
			},
		});
	}

	////////////////////////////////////////////////////
	// Accordion Js
	if ($(".accordion-item").length > 0) {
		$(".accordion-item .faq-title").on("click", function () {
			if ($(this).parent().hasClass("active")) {
				$(this).parent().removeClass("active");
			} else {
				$(this).parent().siblings().removeClass("active");
				$(this).parent().addClass("active");
			}
		});
	}

	////////////////////////////////////////////////////
	// Backtotop Js
	function back_to_top() {
		var btn = $("#back_to_top");
		var btn_wrapper = $(".back-to-top-wrapper");

		$(window).on("scroll", function () {
			if ($(window).scrollTop() > 300) {
				btn_wrapper.addClass("back-to-top-btn-show");
			} else {
				btn_wrapper.removeClass("back-to-top-btn-show");
			}
		});

		btn.on("click", function (e) {
			e.preventDefault();
			$("html, body").animate({ scrollTop: 0 }, "300");
		});
	}
	back_to_top();

	////////////////////////////////////////////////////
	// Odometer js
	if (jQuery(".odometer").length > 0) {
		var om = jQuery(".odometer");
		om.each(function () {
			jQuery(this).appear(function () {
				var numCount = jQuery(this).attr("data-count");
				jQuery(this).html(numCount);
			});
		});
	}

	////////////////////////////////////////////////////
	// wow js
	function wowController() {
		if ($(".wow").length > 0) {
			new WOW().init();
		}
	}

	////////////////////////////////////////////////////
	// VenoBox Js
	if ($(".gallery").length > 0) {
		new VenoBox({
			selector: ".gallery",
			numeration: true,
			// infinigall: true,
			spinner: "pulse",
		});
	}

	if ($(".video-popup").length > 0) {
		new VenoBox({
			selector: ".video-popup",
			numeration: true,
			// infinigall: true,
			spinner: "pulse",
		});
	}

	////////////////////////////////////////////////////
	// Project Hover active change
	if ($(".team-wrapper").length) {
		$(".team-item").on("mouseover", function () {
			// Remove active class from all siblings
			$(this).siblings(".team-item").removeClass("active");

			// Add active class to hovered item
			$(this).addClass("active");

			// Update image dynamically
			const newSrc = $(this).data("src");
			const $image = $("#team-img img");

			// Animate zoom out, change image, then zoom back in
			$image
				.fadeOut(300)
				.css("transform", "scale(1.1)")
				.promise()
				.done(function () {
					$image.attr("src", newSrc).fadeIn(300).css("transform", "scale(1)");
				});
		});
	}

	////////////////////////////////////////////////////
	// progress bar
	const progressBarController = () => {
		const progressContainers = document.querySelectorAll(".tj-progress");

		if (progressContainers?.length) {
			progressContainers.forEach(progressContainer => {
				const targetedProgressBar =
					progressContainer.querySelector(".tj-progress-bar");
				const completedPercent =
					parseInt(targetedProgressBar.getAttribute("data-percent", 10)) || 0;

				// Trigger animation when the element comes into view
				const observer = new IntersectionObserver(
					entries => {
						entries.forEach(entry => {
							if (entry.isIntersecting) {
								// Animate the progress bar
								targetedProgressBar.style.transition = "width 2s ease-out";
								targetedProgressBar.style.width = `${completedPercent}%`;

								// Animate the percentage text
								const percentageText = progressContainer.querySelector(
									".tj-progress-percent"
								);
								if (percentageText) {
									let currentPercent = 0;

									const interval = setInterval(() => {
										currentPercent++;
										percentageText.textContent = `${currentPercent}%`;

										if (currentPercent >= completedPercent) {
											clearInterval(interval); // Stop the animation
										}
									}, 15); // Adjust the interval for animation speed
								}
							}
						});
					},
					{
						root: null, // Observing the viewport
						threshold: [0.3, 0.9], // Progress triggers based on visibility
					}
				);
				observer.observe(progressContainer);
			});
		}
	};

	// Call the function
	progressBarController();

	////////////////////////////////////////////////////
	/* ------------- Circle Proggess Bar Js -------------*/

	if (typeof $.fn.knob != "undefined") {
		$(".knob").each(function () {
			var $this = $(this),
				knobVal = $this.attr("data-rel");

			$this.knob({
				draw: function () {
					$(this.i).val(this.cv + "%");
				},
			});

			$this.appear(
				function () {
					$({
						value: 0,
					}).animate(
						{
							value: knobVal,
						},
						{
							duration: 2000,
							easing: "swing",
							step: function () {
								$this.val(Math.ceil(this.value)).trigger("change");
							},
						}
					);
				},
				{
					accX: 0,
					accY: -150,
				}
			);
		});
	}

	/* ------------- Gsap Js -------------*/
	gsap.registerPlugin(ScrollTrigger, TweenMax, ScrollToPlugin);

	gsap.config({
		nullTargetWarn: false,
	});
	function gsapController() {
		/* ------------- Positon Sticky Js -------------*/

		function initStickySidebar() {
			if (window.innerWidth >= 992) {
				ScrollTrigger.getAll().forEach(trigger => trigger.kill());
				const startPoint = window.innerWidth >= 992 ? 100 : 120;
				gsap.to(".tj-sticky", {
					scrollTrigger: {
						trigger: ".tj-sticky",
						start: `top ${startPoint}`,
						end: `bottom ${startPoint}`,
						pin: true,
						scrub: 1,
					},
				});
			}
		}
		initStickySidebar();
		window.addEventListener("resize", () => {
			initStickySidebar();
		});

		/* Service js */
		let device_width = window.innerWidth;
		const serviceStack = gsap.utils.toArray(".service-stack");
		if (serviceStack.length > 0) {
			if (device_width > 767) {
				serviceStack.forEach(item => {
					gsap.to(item, {
						opacity: 0,
						scale: 0.9,
						y: 50,
						scrollTrigger: {
							trigger: item,
							scrub: true,
							start: "top top",
							pin: true,
							pinSpacing: false,
							markers: false,
						},
					});
				});
			}
		}

		const h6ProjectStack = gsap.utils.toArray(".project-stack");
		if (h6ProjectStack.length > 0) {
			if (device_width > 991) {
				h6ProjectStack.forEach(item => {
					gsap.to(item, {
						// opacity: 0,
						// scale: 0.9,
						// y: 50,
						scrollTrigger: {
							trigger: item,
							scrub: true,
							start: "top top",
							pin: true,
							pinSpacing: false,
							markers: false,
						},
					});
				});
			}
		}

		// Scroll Slider Animation
		if ($(".tj-scroll-slider-item").length > 0) {
			let mediaMatch = gsap.matchMedia();
			mediaMatch.add("(min-width: 768px)", () => {
				const slider = document.querySelector(".tj-scroll-slider");
				if (slider?.children?.length) {
					let panels = gsap.utils.toArray(".tj-scroll-slider-item");
					gsap.to(panels, {
						xPercent: -100 * (panels.length - 1),
						ease: "none",
						scrollTrigger: {
							trigger: slider,
							start: "top+=50 top",
							pin: true,
							scrub: 1,
							end: () => "+=" + slider.offsetWidth,
						},
					});

					// Optional: refresh after setup
					setTimeout(() => ScrollTrigger.refresh(), 500);
				}
			});
		}

		// Sticky Pannel Animation
		if ($(".tj-sticky-panel").length > 0) {
			let mediaMatch = gsap.matchMedia();
			mediaMatch.add("(min-width: 1200px)", () => {
				let tl = gsap.timeline();
				let panels = document.querySelectorAll(".tj-sticky-panel"); // likely the selector being obfuscated
				panels.forEach((panel, i) => {
					tl.to(panel, {
						scrollTrigger: {
							trigger: panel,
							pin: panel,
							scrub: 1,
							start: "top-=50 top",
							end: "bottom top",
							endTrigger: ".tj-sticky-panel-container",
							pinSpacing: false,
							markers: false,
						},
					});
				});
			});
		}

		/* Text Effect Animation */
		if ($(".text-anim").length) {
			let staggerAmount = 0.02,
				translateXValue = 20,
				delayValue = 0.1,
				easeType = "power2.out",
				animatedTextElements = document.querySelectorAll(".text-anim");

			animatedTextElements.forEach(element => {
				let animationSplitText = new SplitText(element, {
					type: "chars, words",
				});
				gsap.from(animationSplitText.chars, {
					duration: 1,
					delay: delayValue,
					x: translateXValue,
					autoAlpha: 0,
					stagger: staggerAmount,
					ease: easeType,
					scrollTrigger: { trigger: element, start: "top 85%" },
				});
			});
		}

		/* Title Animation */
		// if ($(".title-anim").length) {
		// 	let staggerAmount = 0.01,
		// 		delayValue = 0.1,
		// 		easeType = "power1.inout",
		// 		animatedTitleElements = document.querySelectorAll(".title-anim");

		// 	animatedTitleElements.forEach(element => {
		// 		let animatedTitleElements = new SplitText(element, {
		// 			types: "lines, words",
		// 		});
		// 		gsap.from(animatedTitleElements.chars, {
		// 			y: "100%",
		// 			duration: 0.5,
		// 			delay: delayValue,
		// 			autoAlpha: 0,
		// 			stagger: staggerAmount,
		// 			ease: easeType,
		// 			scrollTrigger: { trigger: element, start: "top 85%" },
		// 		});
		// 	});
		// }

		/* Marque js */
		gsap.to(".marquee-slider-wrapper-two", {
			scrollTrigger: {
				trigger: ".tj-project-section-two",
				start: "top center-=200",
				pin: ".marquee-slider-wrapper-two",
				end: "bottom bottom-=200",
				markers: false,
				pinSpacing: false,
				scrub: 1,
			},
		});
		// Marquee slider Js
		if ($(".h5-maquee-slider").length > 0) {
			var swiper = new Swiper(".h5-maquee-slider", {
				slidesPerView: "auto",
				spaceBetween: 30,
				loop: true,
				speed: 5000,
				breakpoints: {
					768: {
						spaceBetween: 35,
					},

					1024: {
						spaceBetween: 50,
					},
				},
				allowTouchMove: false,
				autoplay: {
					delay: 1,
					disableOnInteraction: true,
				},
			});
		}

		// right swipe
		document.querySelectorAll(".rightSwipeWrap").forEach((wrap, i) => {
			gsap.set(wrap.querySelectorAll(".right-swipe"), {
				transformPerspective: 1200,
				x: "10rem",
				rotateY: -20,
				opacity: 0,
				transformOrigin: "right center",
			});
			gsap.to(wrap.querySelectorAll(".right-swipe"), {
				transformPerspective: 1200,
				x: 0,
				rotateY: 0,
				opacity: 1,
				delay: 0.3,
				ease: "power3.out",
				scrollTrigger: {
					trigger: wrap,
					start: "top 80%",
					id: "rightSwipeWrap-" + i,
					toggleActions: "play none none none",
					// markers: true,
				},
			});
		});

		// left swipe
		document.querySelectorAll(".leftSwipeWrap").forEach((wrap, i) => {
			gsap.set(wrap.querySelectorAll(".left-swipe"), {
				transformPerspective: 1200,
				x: "-10rem",
				rotateY: 20,
				opacity: 0,
				transformOrigin: "left center",
			});
			gsap.to(wrap.querySelectorAll(".left-swipe"), {
				transformPerspective: 1200,
				x: 0,
				rotateY: 0,
				opacity: 1,
				delay: 0.4,
				ease: "power3.out",
				scrollTrigger: {
					trigger: wrap,
					start: "top 80%",
					id: "leftSwipeWrap-" + i,
					toggleActions: "play none none none",
					// markers: true,
				},
			});
		});

		// Parallax GSAP
		document.querySelectorAll(".tjParallaxSection").forEach((section, i) => {
			const image = section.querySelector(".tjParallaxImage");
			if (image) {
				gsap.to(image, {
					y: "-25%",
					ease: "none",
					scrollTrigger: {
						trigger: section,
						start: "top bottom",
						end: "bottom top",
						scrub: true,
						// id: "parallax-" + i, // optional for debugging
						// markers: true,
					},
				});
			}
		});

		// itemScrollAnimation
		const teamItems = document.querySelectorAll(".itemScrollAnimate");
		teamItems.forEach((item, index) => {
			const isEven = index % 2 === 0;
			gsap.fromTo(
				item,
				{
					transform: isEven
						? "perspective(1000px) rotateX(50deg)"
						: "perspective(1000px) rotateX(-50deg)",
				},
				{
					transform: isEven
						? "perspective(1000px) rotateX(0deg)"
						: "perspective(1000px) rotateX(0deg)",
					duration: 2,
					ease: "power3.out",
					scrollTrigger: {
						id: `teamItemTrigger-${index}`,
						trigger: item,
						start: "top 100%",
						end: "top 40%",
						scrub: true,
						// markers: true,
					},
				}
			);
		});

		// project drag js
		const $cursor = $(".tj-cursor");
		const $container = $(".project-slider-one");

		if ($container.length > 0) {
			// Center the cursor
			gsap.set($cursor, { xPercent: -50, yPercent: -50 });

			// Track pointer movement
			$(document).on("pointermove", function (e) {
				gsap.to($cursor, {
					duration: 0,
					x: e.clientX,
					y: e.clientY,
				});
			});

			// Show cursor on enter
			$container.on("mouseenter", function () {
				$cursor.css({
					opacity: 1,
					visibility: "visible",
				});
			});

			// Hide cursor on leave
			$container.on("mouseleave", function () {
				$cursor.css({
					opacity: 0,
					visibility: "hidden",
				});
			});
		}

		// Text Invert
		if ($(".tj-text-invert").length) {
			const split = new SplitText(".tj-text-invert", { type: "lines" });
			split.lines.forEach(target => {
				gsap.to(target, {
					backgroundPositionX: 0,
					ease: "none",
					scrollTrigger: {
						trigger: target,
						scrub: 1,
						start: "top 75%",
						end: "bottom center",
					},
				});
			});
		}

		// Text Highlight
		if ($(".title-highlight").length) {
			const highlightText = new SplitText(".title-highlight", {
				type: "lines",
				linesClass: "line",
			});

			const tl = gsap.timeline({
				scrollTrigger: {
					trigger: ".title-highlight",
					scrub: 1,
					start: "top 80%",
					end: "bottom center",
				},
			});
			tl.to(".line", {
				"--highlight-offset": "100%",
				stagger: 0.4,
			});
		}
	}
	// portfolio tabs
	$(".h6-project .h6-project-item").on("mouseover", function () {
		$(this).addClass("active").siblings().removeClass("active");
	});

	// Active on  hover
	if ($(".tj-hover-active-item").length) {
		const allHoverItems = document.querySelectorAll(".tj-hover-active-item");
		allHoverItems.forEach((hoverItem, idx) => {
			hoverItem.addEventListener("mouseenter", function () {
				allHoverItems.forEach((hoverItem2, idx) => {
					hoverItem2?.classList?.remove("active");
				});
				this?.classList?.add("active");
			});
		});
	}

	// Hover bg animation
	function hoverWidget_animation() {
		let active_bg = $(".tj-active-bg-wrapper .active-bg");
		let element = $(".tj-active-bg-wrapper .current");
		$(".tj-active-bg-wrapper .tj-active-bg-item").on("mouseenter", function () {
			let e = $(this);
			activeHover(active_bg, e);
		});
		$(".tj-active-bg-wrapper").on("mouseleave", function () {
			element = $(".tj-active-bg-wrapper .current");
			activeHover(active_bg, element);
			element.closest(".tj-active-bg-item").siblings().removeClass("mleave");
		});
		activeHover(active_bg, element);
		function activeHover(active_bg, e) {
			if (!e.length) {
				return false;
			}
			let topOff = e.offset().top;
			let height = e.outerHeight();
			let menuTop = $(".tj-active-bg-wrapper").offset().top;
			e.closest(".tj-active-bg-item").removeClass("mleave");
			e.closest(".tj-active-bg-item").siblings().addClass("mleave");
			active_bg.css({ top: topOff - menuTop + "px", height: height + "px" });
		}

		$(".tj-active-bg-wrapper .tj-active-bg-item").on("click", function () {
			$(".tj-active-bg-wrapper .tj-active-bg-item").removeClass("current");
			$(this).addClass("current");
		});
	}
	hoverWidget_animation();

	// image slider
	const tjSliderImages = document.querySelectorAll(".tj-image-slider img");

	if (tjSliderImages?.length) {
		let index = 0;
		function showNextImage() {
			tjSliderImages.forEach(img => img.classList.remove("active"));
			tjSliderImages[index].classList.add("active");
			index = (index + 1) % tjSliderImages.length;
		}

		// Initial display
		showNextImage();
		setInterval(showNextImage, 500);
	}
})(jQuery);
