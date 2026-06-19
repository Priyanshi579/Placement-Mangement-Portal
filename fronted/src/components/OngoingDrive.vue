<template>
    <div>
        <h1 style = "text-align: center;">List of Drives</h1>
        <div class = "table" style = "text-align: center;">
            <table border = "10px" bordlinecolor="white" style="margin: auto; border-collapse: collapse;">
                <thead>
                    <tr>
                        <td style="padding: 10px 40px;">Name</td>
                        <td style="padding: 10px 40px;">Action</td>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for = "drive in ongoingdrives" :key = "drive.id">
                        <td style="padding: 15px 40px;">{{drive.name}} </td>
                        <td style="padding: 15px 40px;"><span><button class="btn btn-primary"  @click='this.$router.push(`/update_drive/${drive.id}`)'>view details</button>
                            <button v-if = "drive.status === 'Pending'" class="btn btn-success" style="margin-left: 10px;" @click="mark_as_completed(drive.id)">Mark as Completed</button></span></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>
<script>
import axios from 'axios'
export default{
    name:'OngoingDrive',

    data(){
        return{
            ongoingdrives:[]
        }
    },
    methods:{
        async fetchdrivedetails(){
            const token = localStorage.getItem('token')
            const res = await axios.get('http://localhost:5000/api/company/drive',{
                headers:{
                    Authorization: `Bearer ${token}`
                }
            });
            this.ongoingdrives = res.data
            
        },
        async viewdetails(id){
            const token = localStorage.getItem('token')
            const res = await axios.post(`http://localhost:5000/api/company/drive_details/${id}`,{},{
                headers:{
                    Authorization:`Bearer ${token}`
                }
            })
        },
        async mark_as_completed(id){
            const token = localStorage.getItem('token')
            const res = await axios.post(`http://localhost:5000/api/drive/mark_as_completed/${id}`,{},{
                headers:{
                    Authorization:`Bearer ${token}`
                }
            });
            const targetDrive = this.ongoingdrives.find(drive => drive.id === id);
            if (targetDrive) {
                    targetDrive.status = 'Completed';
                }
                
                alert("Drive marked as completed successfully!");
            }
        },
    mounted(){
        this.fetchdrivedetails()
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