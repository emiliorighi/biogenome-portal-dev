<template>
    <b-container class="router-container" fluid>
        <b-row>
            <b-col>
                <tree-list-component v-if="tree" class="tree-wrapper" :item="tree"></tree-list-component>
            </b-col>
        </b-row>
    </b-container>
</template>
<script>
import TreeListComponent from "./TreeListComponent.vue"


export default {
    computed: {
        tree(){
            return this.$store.getters['portal/getState'].tree
        }
    },
    mounted(){
        if(this.tree === null){
            this.$store.commit('portal/setTree',{value: 'Eukaryota'})
        }
    },
    components:{
        TreeListComponent
    }
}
</script>
<style>
@media screen and (max-width: 600px){
    .tree-wrapper{
        height: 33vh;
    }
}
@media screen and (min-width: 992px){
.tree-wrapper  {
    height: 70vh;
}
}
.tree-wrapper  {
    cursor: pointer;
    list-style-type: none;
    overflow: auto;
}
</style>
