webix.ready(function(){
    webix.ui({
        container: "tabel",
        type: "space",
        rows:[
            { cols:[
                { view:"text", label:"Cari Data:", placeholder:"tanggal, admin, dan aktivitas", id:"filter-table", maxwidth: 300 },
                {}
              ]
            },
            { 
            id: "tabel",
            css:"webix_data_border webix_header_border",
            view: "datatable",
            autoheight: true,
            minHeight: 180,
            autowidth: true,
            url: "https://backend-randy-5zn7xh2gqq-et.a.run.app/data-riwayat",
            columns:[
                { id: "index",    header: "No",    sort: "int", maxWidth: 35 },
                { id: 'id', hidden:true },
                { id: "tanggal",  
                  header: "Tanggal",  
                  sort: "string", 
                  minWidth: 180, 
                  template: 
                    //   ubah format tanggal
                    function(obj){
                        return webix.Date.dateToStr("%d/%m/%Y %H:%i:%s")(obj.tanggal);
                    }
                },
                { id: "admin",   header: "Admin",    sort: "string", maxWidth: 150},
                { id: "aktivitas",   header: "Aktivitas", minWidth: 300},
                { id:"aksi", header:"Aksi", template: "{common.hapus}", maxWidth: 80, css: "pointer" }
            ],
            type: {
                hapus: "<button class='hapus'><i class='webix_icon wxi-trash'></i></button>"
            },
            onClick: {
                hapus:function(){
                    // mengambil id dari row yang diklik tombol hapus
                    var item_id = $$("tabel").getSelectedId();
                    // mengambil id dari data row yang diklik
                    var value = $$("tabel").getItem(item_id);
                    console.log(item_id)
                    console.log(value.id)

                    if (item_id){
                        // menampilkan konfirmasi sebelum menghapus data
                        webix.confirm({
                        title: "Konfirmasi",
                        text: "Apakah anda yakin ingin menghapus data ini?",
                        ok:"Ya", cancel:"Tidak"
                        }).then(function(){
                        // mengirim request ke server untuk menghapus data
                            webix.send("/riwayat", {"id": value.id}, "POST");
                        })
                    }
                }
            },
            scheme: {
                $init:function(obj){ obj.index = this.count(); }
            },
            on: {
                onBeforeLoad:function(){
                    this.showOverlay("Loading...");
                },
                    
                onAfterLoad: function() {
                    this.hideOverlay();
                    if(!this.count()) {
                        this.showOverlay("Maaf, data tidak tersedia");
                    }
                }
            },
            select: true,
            pager: "pager",
        },
        {
            view:"pager",
            id:"pager",
            size:5,
            group:3,
            template:"{common.first()}{common.prev()}{common.pages()}{common.next()}{common.last()}"
        }
        ]
    });

    $$("filter-table").attachEvent("onTimedKeypress", function(){
        var text = this.getValue().toString().toLowerCase();
        //after text entering - filter related grid
        $$("tabel").filter(function(obj){
            //filter by multiple properties
            var filter = [obj.tanggal, obj.admin, obj.aktivitas].join("|");
            filter = filter.toString().toLowerCase();
            return (filter.indexOf(text) != -1);
        });
    });
});