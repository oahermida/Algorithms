package com.algoritmos.ordenamiento;

import java.util.Arrays;
// Source: My dad

public class MergeSort {

	public static void main(String[] args) {

		// Array que queremos ordenar
		int[] A = { 5, 2, 4, 6, 1, 3 };

		// Mostramos el array original
		System.out.println("Antes:");
		System.out.println(Arrays.toString(A));

		// Llamamos al método Merge Sort.
		// El método va a dividir y ordenar el array.
		mergeSort(A);

		// Mostramos el array una vez ordenado
		System.out.println("Después:");
		System.out.println(Arrays.toString(A));
	}

	/*
	 * ========================================================== MÉTODO MERGE SORT
	 * ==========================================================
	 *
	 * Este método utiliza la técnica de "divide y vencerás".
	 *
	 * 1. Divide el array en dos partes. 2. Ordena cada parte mediante recursividad.
	 * 3. Une las dos partes ya ordenadas.
	 *
	 */
	public static void mergeSort(int[] A) {

		/*
		 * CASO BASE DE LA RECURSIVIDAD y condición de salida
		 *
		 * Si el array tiene 0 o 1 elemento, ya está ordenado.
		 *
		 * Por ejemplo:
		 *
		 * [5] -> ya está ordenado [2] -> ya está ordenado
		 *
		 * En ese caso terminamos esta llamada al método.
		 */
		if (A.length <= 1) {
			return;
		}

		/*
		 * Calculamos la posición del medio.
		 *
		 * Por ejemplo, si tenemos:
		 *
		 * [5, 2, 4, 6, 1, 3]
		 *
		 * A.length = 6
		 *
		 * mid = 6 / 2 = 3 --> como mid es un entero si la cantidad de elemento es 
		 * impar se descarta la fracición
		 */
		int mid = A.length / 2;

		/*
		 * Creamos los dos arrays que van a contener la mitad izquierda y la mitad
		 * derecha.
		 *
		 * left -> tendrá "mid" elementos right -> tendrá los elementos restantes
		 */
		int[] left = new int[mid];
		int[] right = new int[A.length - mid];

		/*
		 * Copiamos la primera mitad de A en left.
		 *
		 * Ejemplo:
		 *
		 * A = [5, 2, 4, 6, 1, 3]
		 *
		 * left = [5, 2, 4]
		 */
		for (int i = 0; i < mid; i++) {
			left[i] = A[i];
		}

		/*
		 * Copiamos los elementos restantes en right.
		 *
		 * Ejemplo:
		 *
		 * A = [5, 2, 4, 6, 1, 3]
		 *
		 * right = [6, 1, 3]
		 *
		 * Usamos i - mid para comenzar a llenar right desde la posición 0 
		 * (el elemento 0 de right es mid ya que los arrays son de base 0 en java, 
		 * es decir un array de 6 elementos va de 0 a 5 A[0] a A [5]);
		 */
		for (int i = mid; i < A.length; i++) {
			right[i - mid] = A[i];
		}

		/*
		 * ====================================================== RECURSIVIDAD
		 * ======================================================
		 *
		 * Ahora hacemos exactamente lo mismo con la mitad izquierda.
		 *
		 * Por ejemplo:
		 *
		 * [5, 2, 4]
		 *
		 * se vuelve a dividir en:
		 *
		 * [5] [2, 4]
		 *
		 * Y [2, 4] se vuelve a dividir en:
		 *
		 * [2] [4]
		 *
		 * La recursividad continúa hasta llegar a arrays de un solo elemento.
		 */
		mergeSort(left);

		/*
		 * Hacemos exactamente lo mismo con la mitad derecha.
		 *
		 * Por ejemplo:
		 *
		 * [6, 1, 3]
		 *
		 * se divide en:
		 *
		 * [6] [1, 3]
		 *
		 * y después:
		 *
		 * [1] [3]
		 */
		mergeSort(right);

		/*
		 * ====================================================== UNIÓN DE LAS DOS
		 * MITADES ======================================================
		 *
		 * Cuando mergeSort(left) y mergeSort(right) terminan, tenemos dos arrays
		 * ORDENADOS.
		 *
		 * Por ejemplo:
		 *
		 * left = [2, 4, 5] right = [1, 3, 6]
		 *
		 * Ahora merge() los combina en:
		 *
		 * [1, 2, 3, 4, 5, 6]
		 */
		merge(A, left, right);
	}

	/*
	 * ======================= MÉTODO MERGE =====================
	 * ==========================================================
	 *
	 * Este método recibe:
	 *
	 * A -> array donde vamos a guardar el resultado left -> mitad izquierda, ya
	 * ordenada right -> mitad derecha, ya ordenada
	 *
	 * Su trabajo es comparar los elementos de left y right y colocarlos en A de
	 * menor a mayor.
	 */
	public static void merge(int[] A, int[] left, int[] right) {

		/*
		 * i recorre el array left.
		 *
		 * j recorre el array right.
		 *
		 * k indica en qué posición de A vamos a escribir.
		 *
		 * Al comenzar, los tres están en la posición 0.
		 */
		int i = 0;
		int j = 0;
		int k = 0;

		/*
		 * Mientras todavía haya elementos disponibles tanto en left como en right,
		 * comparamos.
		 */
		while (i < left.length && j < right.length) {

			/*
			 * Comparamos el elemento actual de left con el elemento actual de right.
			 *
			 * Si el de left es menor o igual, lo copiamos en A.
			 */
			if (left[i] <= right[j]) {

				A[k] = left[i];

				// Avanzamos en left
				i++;

			} else {

				/*
				 * Si el elemento de right es menor, copiamos ese elemento en A.
				 */
				A[k] = right[j];

				// Avanzamos en right
				j++;
			}

			/*
			 * Independientemente de qué elemento copiamos, avanzamos a la siguiente
			 * posición de A.
			 */
			k++;
		}

		/* Tomar en cuenta que no se inicializan las variable i y j, quedan
		 * con los valores con que salen de los loops anteriores (while)
		 * 
		 * 
		 * 
		 * ================= ELEMENTOS RESTANTES DE LEFT ================ 
		 * ==============================================================
		 *
		 * Puede ocurrir que right se termine primero.
		 *
		 * Por ejemplo:
		 *
		 * left = [2, 4, 5] right = [1, 3]
		 *
		 * Después de algunas comparaciones puede quedar:
		 *
		 * left = [5]
		 *
		 * En ese caso copiamos los elementos restantes de left
		 * solo va a entrar en este loop si i es menor al largo de 
		 * left, es decir solo si quedaron elementos restantes en left.
		 */
		while (i < left.length) {

			A[k] = left[i];

			i++;
			k++;
		}

		/*
		 * ================ ELEMENTOS RESTANTES DE RIGHT ====
		 * ==================================================
		 *
		 * Lo mismo puede ocurrir al revés:
		 *
		 * que left se termine antes que right.
		 *
		 * Entonces copiamos los elementos que quedan en right
		 * solo va a entrar en este en este loop si j es menor al largo de 
		 * right, es decir solo si quedaron elementos restantes en right.
		 */
		while (j < right.length) {

			A[k] = right[j];

			j++;
			k++;
		}
	}
}