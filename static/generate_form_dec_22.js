 const categories_div = document.querySelector("#categories_container")
        let category_count = 0


        const all_elements = {
            'main_categories': {}
        }

        const
            generate_category_div = (category_number) => {
                return `
                <div class="row" id="category-${category_number}-row">
                    <div class="col-lg-12">

                        <label for="category-${category_number}">Category name</label>
                            <div class="row">
                                <div class="col-lg-9 mb-2">
                                    <input id='category-${category_number}-input' class="form-control" name='category-${category_number}-name' type="text">
                                </div>
                                <div class="col-lg-3">
                                    <button onclick="replace_main_category_with_accordion(event)" data-category_number=${category_number} data-row_id="category-${category_number}-row" class="btn btn-primary ">
                                        Add
                                    </button>

                                    <button onclick="delete_div(event)"  data-row_id="category-${category_number}-row"  class="btn btn-danger">
                                        Delete
                                    </button>
                            </div>
                        </div>

                    </div>
                </div>
            `
            }

        {# Main category = category #}
        {# Category = sub category #}
        {# sub category = field #}


        function addCategory() {
            categories_div.innerHTML += generate_category_div(category_count + 1)
            category_count += 1
        }


        function replace_main_category_with_accordion(e) {
            const category_num = e.target.dataset.category_number
            const row_target = e.target.dataset.row_id
            const input_val = document.getElementById(`category-${category_num}-input`).value
            all_elements.main_categories[category_num] = {
                'name': input_val,
                'sub_category_count': 0,
                'sub_categories': {}
            }
            const accordion_html = `
                  <div class="col-lg-12">
                    <div id="accordionForm">
                        <div class="card mb-2">
                            <div class="card-header" id="headingOne">
                              <h5 class="mb-0">
                                <button class="btn btn-link" data-toggle="collapse" data-target="#collapse-${category_num}" aria-expanded="true" aria-controls="collapse-${category_num}">
                                  ${input_val}
                                </button>
                                <button class="btn btn-danger float-right" data-category_id=${category_num}>
                                  <i class="fa fa-trash"></i>&nbsp;
                                   <span>Delete</span>
                                </button>
                              </h5>
                            </div>

                            <div id="collapse-${category_num}" class="collapse show" aria-labelledby="headingOne" data-parent="#accordionForm">
                              <div class="card-body">
                                <div class="row">
                                    <div class="col-lg-12" id="category-${category_num}-subcategories">

                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-3 ml-auto">
                                        <button data-category_num=${category_num} data-target_sub_cat_container="category-${category_num}-subcategories" onclick="addSubCategory(event)" class="btn btn-primary float-right">
                                        <i class="fa fa-plus"></i>&nbsp;
                                        Add sub category
                                        </button>
                                    </div>
                                </div>
                              </div>
                            </div>
                      </div>
                    </div>
                  </div>
            `
            const row_elem = document.getElementById(row_target)
            row_elem.innerHTML = accordion_html
        }

        function delete_div(e) {
            const row_id = e.target.dataset.row_id
            const node = document.getElementById(row_id)

            node.parentNode.removeChild(node)
        }

        function generate_subcategory_div(category, sub_category_number) {
            return `
                <div class="row" id="category-${category}-subcategory-${sub_category_number}">
                    <div class="col-lg-12">

                        <label for="category-${category}-subcategory-${sub_category_number}-input">Category name</label>
                            <div class="row">
                                <div class="col-lg-9 mb-2">
                                    <input id='category-${category}-subcategory-${sub_category_number}-input' class="form-control" name='category-${category}-subcategory-${sub_category_number}-name' type="text">
                                </div>
                                <div class="col-lg-3">
                                    <button  data-category_number=${category} data-sub_category_number=${sub_category_number}  data-row_id="category-${category}-subcategory-${sub_category_number}-row" class="btn btn-primary ">
                                        Add
                                    </button>

                                    <button onclick="delete_div(event)"  data-row_id="category-${category}-subcategory-${sub_category_number}"  class="btn btn-danger">
                                        Delete
                                    </button>
                            </div>
                        </div>

                    </div>
                </div>
            `
        }

        function addSubCategory(e) {
            console.log(e.target)
            let target_sub_cat_container = document.getElementById(e.target.dataset.target_sub_cat_container)
            let category_num = e.target.dataset.category_num

            console.log(all_elements, category_num)
            all_elements.main_categories[category_num].sub_category_count += 1

            target_sub_cat_container.innerHTML += generate_subcategory_div(category_num, all_elements.main_categories[category_num].sub_category_count)

        }


        /*
        window.onbeforeunload = function (e) {
            return "Please click 'Stay on this Page' if you did this unintentionally";
        };*/