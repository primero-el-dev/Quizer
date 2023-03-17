const CSRF_TOKEN = document.getElementById('csrf_token').value
const POINT_CATEGORY_REGEX = /(?<=point_categories\-)(\d+)(?=\-)/

const insertPointCategory = () => {
    let i = document.querySelectorAll('.point-category')['length']
    let element = `<div class="point-category card border border-dark">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="d-inline-block">Point category</h5>
                <span>
                    <button type="button" class="move-up-point-category btn btn-mini btn-primary ml-auto" onclick="moveUpPointCategory(event)">Move up</button>
                    <button type="button" class="move-down-point-category btn btn-mini btn-primary ml-4" onclick="moveDownPointCategory(event)">Move down</button>
                    <button type="button" class="delete-point-category btn btn-mini btn-danger ml-4" onclick="deleteClosestPointCategory(event)">Delete</button>
                </span>
            </div>
            <div class="card-body">
                <input type="hidden" name="point_categories-${i}-id" value="${crypto.randomUUID()}">
                <input type="hidden" name="point_categories-${i}-csrf_token" value="${CSRF_TOKEN}">
                <label class="form-group w-100 mb-3">
                    Name
                    <input type="text" name="point_categories-${i}-name" class="form-control" maxlength="255" required>
                </label>
                <label class="form-group w-100 mb-3">
                    Description
                    <textarea name="point_categories-${i}-description" class="form-control" maxlength="4095" required></textarea>
                </label>
            </div>
        </div>`
    
    $('#point-categories').append(element)
}

const moveDownPointCategory = moveDown('.point-category', POINT_CATEGORY_REGEX)
const moveUpPointCategory = moveUp('.point-category', POINT_CATEGORY_REGEX)
const deleteClosestPointCategory = deleteClosest('.point-category', POINT_CATEGORY_REGEX)