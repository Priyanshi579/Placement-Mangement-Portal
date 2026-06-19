<template>
    <div>
        <h1 style = "text-align: center;">List of Company</h1>
        <div class = "table" style = "text-align: center;">
            <table border = "10px" bordlinecolor="white" style="margin: auto; border-collapse: collapse;">
                <thead>
                    <tr>
                        <td style="padding: 10px 40px;">Name</td>
                        <!-- <td style="padding: 10px 40px;">Company</td> -->
                        <td style="padding: 10px 40px;">Date</td>
                        <td style="padding: 10px 40px;">Action</td>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for = "drive in applied_drives" :key = "drive.id">
                        <td style="padding: 15px 40px;">{{drive.name}} </td>

                        <!-- <td style="padding: 15px 40px;">{{drive.company}} </td> -->

                        <td style="padding: 15px 40px;">{{drive.application_date}} </td>

                        <td style="padding: 15px 40px;"><button class="btn btn-primary"  @click="viewdetails_applied(drive.drive_id)">view details</button></td>
                        
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>
<script>
import axios from 'axios'
export default{
    name:'AppliedDrive',
    data(){
        return{
            applied_drives:[]
        }
    },
    methods:{
        async fetchapplydrivedetails(){
            const token = localStorage.getItem('token');
            const res = await axios.get('http://localhost:5000/api/get/applied/drive',{
                headers:{
                    Authorization: `Bearer ${token}`
                }
            });
            console.log(res.data)
            this.applied_drives = res.data
        },
        
        viewdetails_applied(id){
            this.$router.push({name: 'AppliedDriveDetails', params: {drive_id: id}});
            }
    },
    mounted(){
        this.fetchapplydrivedetails()
    }
}
</script>

<style scoped>
    .table{
        border:none;
        margin-top:10px;
        width:715px;
        /* ADD THESE THREE LINES TO CENTER THE CANVAS: */
        display: flex;
        justify-content: center; /* Centers horizontally */
        align-items: flex-start; /* Keeps the canvas layout sticking towards the top */
        /* min-height: 100vh; */
    }
</style>
