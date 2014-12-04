if (typeof gui_if != 'object')
var gui_if = {
	function: function(a, b, c, d, e, f, g, h, i) {
		var jQuery;

		if (window.jQuery === undefined || window.jQuery.fn.jquery !== '2.1.1') {
			var script_tag = document.createElement('script');
			script_tag.setAttribute("type","text/javascript");
			script_tag.setAttribute("src","http://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js");

			script_tag.onload = scriptLoadHandler;

			(document.getElementsByTagName("head")[0] || document.documentElement).appendChild(script_tag);

		} else {
			jQuery = window.jQuery;
			main();
		}

		function scriptLoadHandler() {
			jQuery = window.jQuery.noConflict(true);
			main();
		}

		function main() {
			jQuery(document).ready(function($) {
				// CSS の読み込み
				var css_link = $("<link>", {
					rel: "stylesheet", type: "text/css"
					, href: b + "gui_if/css/gui_if.css"
				});
				css_link.appendTo('head');

				// APIから情報を取得する処理
				function loadHTML(){
					$.getJSON(a + "/access_api?callback=?"
							, {url: c, api_key: d}
							, function(data) {
								$('#' + e).html(data.hashrate);
								$('#' + f).html(data.unit);
								$('#' + g).html(data.credit);
								$('#' + h).html(data.currency);
								$('#' + i).html(data.worker);
							}
					);

				}

				// 画面遷移時と、一定時間ごとに情報を取得する
				loadHTML();
				setInterval(function(){loadHTML();}, 90*1000);
			});
		}
	}
};