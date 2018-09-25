	<html>
		<head>
			<script type="text/javascript">
			// setup some JSON to use

			window.onload = function() {
				// setup the button click
				document.getElementById("theButton").onclick = function() {
					doWork()
				};
			}

			function doWork() {
				var toSend = {'symbol':$('#text').val()}
				// ajax the JSON to the server
				$.post("receiver", JSON.stringify(toSend), function(data){
					var to_print = $.csv.toArrays("{{ url_for('static', filename = 'result.csv') }}")
					alert(to_print)
					var combined_string="";
					jQuery.each(to_print, function(i, val){
						jQuery.each(val, function(i, val){
							combined_string += val + " ";
						})
						combined_string += "<br />"
					})
					$( "#result" ).append("<br>"+combined_string)
				})
				// stop link reloading the page
			event.preventDefault();
			}
			</script>
		</head>
		<body>
			Symbol:<br /><br />
			<input id='text' style='width:75%;height:30px'></input><br>
			<a href="" id="theButton">Predict</a><br>
			Result:<a id="result">
			</a><script src="https://code.jquery.com/jquery-3.3.1.js"></script>
			<script src="{{ url_for('static', filename = 'jquery.csv.js') }}"></script>
		</body>
	</html>

