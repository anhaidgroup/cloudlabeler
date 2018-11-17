/**
 * jquery.simplePagination.js
 * @version: v1.0.0
 * @author: Sebastian Marulanda http://marulanda.me
 * @see: https://github.com/smarulanda/jquery.simplePagination
 */

(function($) {

	$.fn.simplePagination = function(options) {

		var defaults = {
			perPage: 2,
			rowMultiple:3,
			containerClass: '',
			previousButtonClass: '',
			nextButtonClass: '',
			previousButtonText: 'Previous',
			nextButtonText: 'Next',
			currentPage: 1
		};

		var settings = $.extend({}, defaults, options);

		return this.each(function() {
			var $rows = $('tbody tr', this);


			var pages = Math.ceil($rows.length/(settings.perPage*settings.rowMultiple));

			var container = document.createElement('div');
			var bPrevious = document.createElement('button');
			var bNext = document.createElement('button');
			var of = document.createElement('span');

			bPrevious.innerHTML = settings.previousButtonText;
			bNext.innerHTML = settings.nextButtonText;

			container.className = settings.containerClass;
			bPrevious.className = settings.previousButtonClass;
			bNext.className = settings.nextButtonClass;

			bPrevious.style.marginRight = '8px';
			bNext.style.marginLeft = '8px';
			container.style.textAlign = "center";
			container.style.marginBottom = '20px';

			container.appendChild(bPrevious);
			container.appendChild(of);
			container.appendChild(bNext);

			$(this).after(container);

			update();

			$(bNext).click(function() {
				if (settings.currentPage + 1 > pages) {
					settings.currentPage = pages;
				} else {
					settings.currentPage++;
				}

				update();
			});

			$(bPrevious).click(function() {
				if (settings.currentPage - 1 < 1) {
					settings.currentPage = 1;
				} else {
					settings.currentPage--;
				}

				update();
			});

			function update() {
				var from = ((settings.currentPage - 1) * settings.perPage*settings.rowMultiple) + 1;
				var to = from + settings.perPage*settings.rowMultiple - 1;
				//alert('ppp')
				//alert(from)
				//alert(to)

				if (to > $rows.length) {
					to = $rows.length;
				}

				$rows.hide();

				$rows.slice((from-1), to).show();

				of.innerHTML = Math.ceil(from/settings.rowMultiple) + ' to ' + Math.ceil(to/settings.rowMultiple) +
                    ' of ' + Math.ceil($rows.length/settings.rowMultiple) + ' entries';

				if ($rows.length <= settings.perPage) {
					$(container).hide();
				} else {
					$(container).show();
				}
				if(from > to) {
					$(container).hide();
				} else {
					$(container).show();

				}
			}
		});

	}

}(jQuery));
