/* 	
	author: policecar
	date: 	June 17th 2013

	Custom JavaScript mini library that processes a text file containing
	n-grams and visualizes them as graph-like structures using D3.js.

	The data are assumed to be space separated with the last column being
	the counts; e.g. "look at [STH] 126258" or "seem to [SO] {to be} 123647".

	Special thanks go to Moritz Stefaner, as p.makeGraph() is 
	adapted from https://gist.github.com/MoritzStefaner/1377729.
*/ 
p = function() {

	var p = {
		version: "0.0.1"
	};

	p.processFileContent = function( textString ) {

		var lines = textString.split( '\n' );

		var items = {};

		var nodes = {};
		var labelAnchors = [];
		var labelAnchorLinks = [];
		var links = [];

		for ( var i = 0, l; l = lines[i]; i++ ) {
			
			// split into tokens
			var tokens = l.split(' ');
			var count = tokens[ tokens.length-1 ];
			
			var prev = null;
			var node = null;
			var key = null;

			var nodeKey = '';
			var tmp = '';

			for ( var j = 0, t; t = tokens[j]; j++ ) {
				
				if ( j == tokens.length-1 ) { // skip last token - it's a count
					continue;
				}

				// if node with same text and position exists, use that existing node, else create
				tmp = [ t, j ].join('_');
				nodeKey += tmp + '_';
				if ( nodes && nodeKey in nodes ) {
					// if node with same label and position exists, 
					// check if it is connected to same predecessor
					node = nodes[nodeKey];
				} else {
					node = {
						pos: j,
						label: t
					}
					nodes[nodeKey] = node;
					labelAnchors.push({
						node : node
					});
					labelAnchors.push({
						node : node
					});
				}
				
				if ( j > 0 ) { // the first token has no incoming links
					links.push({
						source : prev,
						target : node,
						weight : 1
					});
				}
				prev = node;
			}
		}
		// turn nodes from {} to []
		var nodeArray = [];
		for( var key in nodes ) {
			nodeArray.push( nodes[key] );
		}
		// var linkArray = [];
		// for( var key in links ) {
		// 	linkArray.push( links[key] );
		// }		

		// attach labels
		for( var k = 0; k < nodeArray.length; k++ ) {
			labelAnchorLinks.push({ 
				source : k * 2,
				target : k * 2 + 1, 
				weight : 1 
			});
		}

		// stuff them all into a single object
		items.nodes = nodeArray;
		items.labelAnchors = labelAnchors;
		items.labelAnchorLinks = labelAnchorLinks;
		items.links = links; //linkArray;

		return items;
	};

	p.makeGraph = function( data ) {
		
		var nodes = data.nodes;
		var links = data.links;
		var labelAnchors = data.labelAnchors;
		var labelAnchorLinks = data.labelAnchorLinks;

		// var w = 960, h = 500;
		var w = screen.width, h = screen.height;

		var labelDistance = 0;
		var vis = d3.select("body").append("svg:svg").attr("width", w).attr("height", h);

		var force = d3.layout.force().size([w, h]).nodes(nodes).links(links)
			.gravity(1).linkDistance(50).charge(-3000).linkStrength(function(x) {
			return x.weight * 10
		});

		force.start();

		var force2 = d3.layout.force().nodes(labelAnchors).links(labelAnchorLinks)
			.gravity(0).linkDistance(0).linkStrength(8).charge(-100).size([w, h]);
		force2.start();

		var link = vis.selectAll("line.link").data(links).enter().append("svg:line").attr("class", "link").style("stroke", "#CCC");

		var node = vis.selectAll("g.node").data(force.nodes()).enter().append("svg:g").attr("class", "node");
		node.append("svg:circle").attr("r", 5).style("fill", "#555").style("stroke", "#FFF").style("stroke-width", 3);
		node.call(force.drag);

		var anchorLink = vis.selectAll("line.anchorLink").data(labelAnchorLinks)
			//.enter().append("svg:line").attr("class", "anchorLink").style("stroke", "#999");

		var anchorNode = vis.selectAll("g.anchorNode").data(force2.nodes()).enter().append("svg:g").attr("class", "anchorNode");
		anchorNode.append("svg:circle").attr("r", 0).style("fill", "#FFF");
			anchorNode.append("svg:text").text(function(d, i) {
			return i % 2 == 0 ? "" : d.node.label
		}).style("fill", "#555").style("font-family", "Arial").style("font-size", 12);

		var updateLink = function() {
			this.attr("x1", function(d) {
				return d.source.x;
			}).attr("y1", function(d) {
				return d.source.y;
			}).attr("x2", function(d) {
				return d.target.x;
			}).attr("y2", function(d) {
				return d.target.y;
			});
		}

		var updateNode = function() {
			this.attr("transform", function(d) {
				return "translate(" + d.x + "," + d.y + ")";
			});
		}

		force.on("tick", function() {

			force2.start();
			node.call(updateNode);

			anchorNode.each(function(d, i) {
				if(i % 2 == 0) {
					d.x = d.node.x;
					d.y = d.node.y;
				} else {
					var b = this.childNodes[1].getBBox();

					var diffX = d.x - d.node.x;
					var diffY = d.y - d.node.y;

					var dist = Math.sqrt(diffX * diffX + diffY * diffY);

					var shiftX = b.width * (diffX - dist) / (dist * 2);
					shiftX = Math.max(-b.width, Math.min(0, shiftX));
					var shiftY = 5;
					this.childNodes[1].setAttribute("transform", "translate(" + shiftX + "," + shiftY + ")");
				}
			});

			anchorNode.call(updateNode);
			link.call(updateLink);
			anchorLink.call(updateLink);
		});
	};

	return p;
}();