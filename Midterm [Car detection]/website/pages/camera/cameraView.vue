<script setup lang="ts">
import  carService from '~/composable/carComposable/useTables';

const { infoCar, isLoading, errorMessage, } = carService();

</script>

<template>
  <div class="mt-10">
    <div class="relative overflow-x-auto">
      <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
        <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
          <tr>
            <th scope="col" class="px-6 py-3">
              Number
            </th>
            <th scope="col" class="px-6 py-3">
              Name car
            </th>
            <th scope="col" class="px-6 py-3">
              Date and time
            </th>
          </tr>
        </thead>

        <tbody>
          <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700" v-for="(itemCar, index) in infoCar" :key="index">
            <th>
              {{ itemCar.id }}
            </th>
            
            <td class="px-6 py-4">
              {{ itemCar.title }}
            </td>

            <td>
              {{ itemCar.time }}
            </td>

          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped></style>