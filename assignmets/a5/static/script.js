function setup() {
	document.getElementById("create_cat").addEventListener("click", makeCatPost, true);
	document.getElementById("create_purch").addEventListener("click", makePurchPost, true);
	populateAllCats();
	populateAllPurchs();
}

function makeCatPost() {
	var httpRequest = new XMLHttpRequest();

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}
			
	httpRequest.onreadystatechange = function() { alertResult(httpRequest) };
	
	httpRequest.open("POST", "/cats/");
	httpRequest.setRequestHeader('Content-Type', 'application/json');

	var cat ={name:"name", "limit":0, "spent":0};
	cat.name=document.getElementById("cat_name").value;
	cat.limit=document.getElementById("cat_limit").value;
	cat.spent=document.getElementById("cat_spent").value;
	httpRequest.send(JSON.stringify(cat));
	addCat(cat);
	populateAllCats();
}

function makePurchPost() {
	var httpRequest = new XMLHttpRequest();

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}
			
	httpRequest.onreadystatechange = function() { alertResult(httpRequest) };
	
	httpRequest.open("POST", "/purchs/");
	httpRequest.setRequestHeader('Content-Type', 'application/json');

	var purch ={};
	purch.amount=document.getElementById("purch_amount").value;
	purch.spentOn=document.getElementById("spent_on").value;;
	purch.cat_id= document.getElementById("purch_cats").value;;
	purch.date = (new Date()).toString();
	
	httpRequest.send(JSON.stringify(purch));
	populateAllCats();
	populateAllPurchs();
}

function addCat(cat){
	var status 
	if (cat.limit<cat.spent){
		status = "<font color=\"red\">OverSpent</font>";
	}else{
		status ="Normal";
	}
	
	var cat_list_ul = document.getElementById("cat_list");
	var li = document.createElement("li");
	li.innerHTML = "name: " + cat.name +", limit: " +cat.limit +", spent: " + cat.spent + ", status: " + status;
	var bDelete= document.createElement("input");
	bDelete.setAttribute("type","button");
	bDelete.setAttribute("id",cat.cat_id);
	bDelete.setAttribute("name", cat.cat_id);
	bDelete.setAttribute("value", "Delete");
	bDelete.addEventListener("click", handleDelete, true);
	
	li.appendChild(bDelete);
	
	cat_list_ul.appendChild(li);
	
}

function handleDelete(event){
	var httpRequest = new XMLHttpRequest();
	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}


    event = event || window.event;
    event.target = event.target || event.srcElement;
	var element = event.target;
	
	httpRequest.onreadystatechange = function() { handlePoll(httpRequest) };
	console.log(element.id);
	if (element.id==-1){
		alert('You cannot delete this category.');
		return false;
	}
	httpRequest.open("DELETE", "/cats/"+element.id);
	httpRequest.send();
	populateAllCats();
	populateAllPurchs();
	
}

function addPurch(purch){
	var purch_list_ul = document.getElementById("purch_list");
	var li = document.createElement("li");
	li.innerHTML = "amount: " + purch.amount+", spent_on: " +purch.spentOn+", category: " + document.getElementById("op_"+purch.cat_id).text +", date :" + purch.date;
	purch_list_ul.appendChild(li);
	
}

function alertResult(httpRequest) {
//	alert("ALERTING!  readyState:  " + httpRequest.readyState);
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		console.log(httpRequest.responseText);
//		alert("ALERTING!  status:  " + httpRequest.status);
		if (httpRequest.status === 200) {
//			alert("ALERTING!  Value sent to server!");
		} else {
//			alert("ALERTING!  There was a problem with the request.");
		}
	}
}

function populateAllCats(){
	var httpRequest = new XMLHttpRequest();

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = function() { handlePoll(httpRequest) };
	httpRequest.open("GET", "/cats/");
	httpRequest.send();
}

function handlePoll(httpRequest) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		console.log(httpRequest.responseText);
		if (httpRequest.status === 200) {
			var cats = JSON.parse(httpRequest.responseText);
			
			//fill up category list 
			if (cats.length>0){
				document.getElementById("cat_list").innerHTML="";
				document.getElementById("purch_cats").innerHTML="";
			}
			for (var i = 0; i < cats.length; i++) {
				addCat(cats[i]);
				addCatSelectEl(cats[i]);
			}			
		} else {
//			alert("There was a problem with the poll request.  you'll need to refresh the page to recieve updates again!");
		}
	}
}

function populateAllPurchs(){
	var httpRequest = new XMLHttpRequest();

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = function() { handlePurchPoll(httpRequest) };
	httpRequest.open("GET", "/purchs/");
	httpRequest.send();
}

function handlePurchPoll(httpRequest) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		console.log(httpRequest.responseText);
		if (httpRequest.status === 200) {
			var purchs = JSON.parse(httpRequest.responseText);
			
			//fill up purch
			if (purchs.length>0){
				document.getElementById("purch_list").innerHTML="";
			}
			for (var i = 0; i < purchs.length; i++) {
				addPurch(purchs[i]);
			}			
		} else {
			alert("There was a problem with the poll request.  you'll need to refresh the page to recieve updates again!");
		}
	}
}


function addCatSelectEl(cat){
	var cat_select = document.getElementById("purch_cats");
	var op = document.createElement("option");
	op.setAttribute("value",cat.cat_id);
	op.setAttribute("id","op_"+cat.cat_id);
	op.innerHTML = cat.name;
	cat_select.appendChild(op);
	
}

window.addEventListener("load", setup, true);