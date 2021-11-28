const new_ing = document.getElementById('add-ingredient');

function ingredient_func(event) {
	const recipeList = document.getElementById('recipe');
	const fieldSet = document.createElement('fieldset');
	fieldSet.innerHTML = `
	<hr>

	  <div>
		<input type="text" name="ingredient_name[]" id="ingredient_name" placeholder = "Ingredient Name">
	  </div>
	  <div>
		<input type="number" name="amount[]" id="ingredient_amount" placeholder = "Ingredient Amount">
	  </div>

	  <div>
		<input type="text" name="measurement[]" id="ingredient_measurement" placeholder = "Measurement">
	  </div>`;
	recipeList.append(fieldSet);
}

new_ing.addEventListener('click', ingredient_func);
