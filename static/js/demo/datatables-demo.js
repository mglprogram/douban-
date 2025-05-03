// Call the dataTables jQuery plugin
$(document).ready(function() {
    $('#dataTable').DataTable({
        "columnDefs": [
            { "orderable": false, "targets": [1,2,4,5,6,7,8,9,12,13] }
        ],
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.25/i18n/Chinese.json" // 中文显示
        }
    });
});
