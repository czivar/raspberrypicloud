
var permissionForm = new function () {
	
	var me = this;
	
	var mouseX, mouseY;
	var userNodes, currentlyDraggedNode;
	

	
	me.init = function () {
		if (EventHelpers.hasPageLoadHappened(arguments)) {
			return;
		}
		
		userNodes = cssQuery('[draggable=true]');
		
		for (var i=0; i<userNodes.length; i++) {
			EventHelpers.addEvent(userNodes[i], 'dragstart', userDragStartEvent);
			EventHelpers.addEvent(userNodes[i], 'dragend', userDragEndEvent);
		}

		userListNodes = cssQuery('.userList');
		for (var i=0; i<userListNodes.length; i++) {
			var userListNode = userListNodes[i];
			EventHelpers.addEvent(userListNode, 'dragover', userDragOverListEvent);
			EventHelpers.addEvent(userListNode, 'drop', userDropListEvent);	
		}	
		
	}
	
	function userDragStartEvent(e) {
		e.dataTransfer.setData("Text", this.innerHTML);
		e.dataTransfer.setData("From", $(this).closest("td").attr("id"));
		currentlyDraggedNode = this;				
		currentlyDraggedNode.className = 'draggedUser';
	}
	
	
	function userDragEndEvent(e) {	
		currentlyDraggedNode.className = '';
	}
	
	
	function userDropListEvent(e) {
		/*
		 * To ensure that what we are dropping here is from this page
		 */
		
		var data = e.dataTransfer.getData("Text");
		if (data.indexOf("ip-") != 0) {
			alert("Only machines within this page are draggable.")
		}
		
		currentlyDraggedNode.parentNode.removeChild(currentlyDraggedNode);
		this.appendChild(currentlyDraggedNode);
		userDragEndEvent(e);
		//cool stuff
		var to = $(this).closest("td").attr("id");
		var from = e.dataTransfer.getData("From")
		var url1 = "http://"+to+".dcs.gla.ac.uk:9999/start/"+data;
		var url2 = "http://"+from+".dcs.gla.ac.uk:9999/stop/"+data;
		$.get(url1, function(data, status) {
		}, 'html');
		$.get(url2, function(data, status) {
		}, 'html');
	}
	
	function userDragOverListEvent(e) {	
		EventHelpers.preventDefault(e);
	}
	
	
}

EventHelpers.addPageLoadEvent('permissionForm.init');
