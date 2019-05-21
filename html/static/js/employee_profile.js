//////////////////////////////////////////
// This file contains all functions     //
// used on the profile page             //
//////////////////////////////////////////


$(document).ready(function () {
    initProfileTable();
    initializeTinyMCE();

    /**
     * Creates callback function for editor modal. The callback function activates when the
     * modal pops up.
     * This function fills the modal with the needed data.
     */
    $('#project-editor').on('show.bs.modal', function (e) {
        let title = $(e.relatedTarget).data('title');
        let project_id = $(e.relatedTarget).data('id');
        let desc_nl = $(e.relatedTarget).data('desc-nl');
        let desc_en = $(e.relatedTarget).data('desc-en');
        let desc_nl_id = $(e.relatedTarget).data('desc-nl-id');
        let desc_en_id = $(e.relatedTarget).data('desc-en-id');
        $("#project-editor .modal-body #project-title").val(title);
        $("#project-editor .modal-body #project-id").val(project_id);
        $("#project-editor .modal-body #desc-nl-id").val(desc_nl_id);
        $("#project-editor .modal-body #desc-en-id").val(desc_en_id);
        tinyMCE.get('project-desc-en').setContent(desc_en);
        tinyMCE.get('project-desc-nl').setContent(desc_nl);
        document.getElementById("modal-title").innerHTML = "Edit: " + title;
    });

    /**
     * Creates callback function for the delete modal. The callback function activates when the modal
     * pops up.
     * This function fills the modal with the needed data.
     */
    $('#change-project-active').on('show.bs.modal', function (e) {
        let id = $(e.relatedTarget).data('id');
        let type = $(e.relatedTarget).data('type');

        let title = $('#change-project-active .modal-header .modal-title');
        $('#change-project-active .modal-footer #project-id').val(id);
        switch(type){
            case "activate":
                title.text(activateText);
                break;
            case "deactivate":
                title.text(deactivateText);
                break;
        }
    });

});

/**
 * Initializes the table with projects. The function transforms it into a DataTable
 * and sets its settings
 */
function initProfileTable() {
    $('#profile-table').DataTable({
        "columnDefs": [
            {"bSortable": false, "targets": 0}
        ],
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
        "order": [[0, 'asc'], [1, 'asc']],
        "pageLength": -1,
        "stateSave": true,
        "lengthChange": false,
        "paging": false,
        "info": false
    });
}

/**
 * Initializes the tiny MCE fields on the profile page
 */
function initializeTinyMCE() {
    tinymce.init({
        selector: '#project-desc-nl',
        menubar: 'edit insert format table tools',
        height: '400px'
    });
    tinymce.init({
        selector: '#project-desc-en',
        menubar: 'edit insert format table tools',
        height: '400px'
    });
}