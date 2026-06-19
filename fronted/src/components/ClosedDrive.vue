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
                    <tr v-for = "drive in closeddrives" :key = "drive.id">
                        <td style="padding: 15px 40px;">{{drive.name}} </td>
                        <td style="padding: 15px 40px;"><button class="btn btn-primary"  @click="this.$router.push(`/update_drive/details/${drive.id}`)">Update</button>
                            </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>
<script>
import axios from 'axios'
export default{
    name:'ClosedDrive',

    data(){
        return{
            closeddrives:[]
        }
    },
    methods:{
        async fetchdrivedetails(){
            const token = localStorage.getItem('token');
            const res = await axios.get('http://localhost:5000/api/closed_drives',{
                headers:{
                    Authorization: `Bearer ${token}`
                }
            });
            this.closeddrives = res.data
            
        },
        async updatedetails(id){
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