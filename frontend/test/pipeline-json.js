const pipelineJson = [
  {
    name: 'missingValuesRemove',
    pretty_name: 'missing values removal',
    parameters: {},
    is_highlighted: false,
    models: {
      missingValuesRemove: {
        name: 'missingValuesRemove',
        pretty_name: 'missing values removal',
        parameters: {},
        is_highlighted: false,
      },
      missingValuesFill: {
        name: 'missingValuesFill',
        pretty_name: 'missing values fill',
        parameters: {},
        is_highlighted: false,
      },
      labelRemove: {
        name: 'labelRemove',
        pretty_name: 'labelRemove',
        parameters: {},
        is_highlighted: false,
      },
      oneHotEncode: {
        name: 'oneHotEncode',
        pretty_name: 'oneHotEncode',
        parameters: {},
        is_highlighted: false,
      },
    },
  },
  {
    name: 'labelRemove',
    pretty_name: 'labelRemove',
    parameters: {},
    is_highlighted: false,
    models: {
      missingValuesRemove: {
        name: 'missingValuesRemove',
        pretty_name: 'missing values removal',
        parameters: {},
        is_highlighted: false,
      },
      missingValuesFill: {
        name: 'missingValuesFill',
        pretty_name: 'missing values fill',
        parameters: {},
        is_highlighted: false,
      },
      labelRemove: {
        name: 'labelRemove',
        pretty_name: 'labelRemove',
        parameters: {},
        is_highlighted: false,
      },
      oneHotEncode: {
        name: 'oneHotEncode',
        pretty_name: 'oneHotEncode',
        parameters: {},
        is_highlighted: false,
      },
    },
  },
  {
    name: 'oneHotEncode',
    pretty_name: 'oneHotEncode',
    parameters: {},
    is_highlighted: false,
    models: {
      missingValuesRemove: {
        name: 'missingValuesRemove',
        pretty_name: 'missing values removal',
        parameters: {},
        is_highlighted: false,
      },
      missingValuesFill: {
        name: 'missingValuesFill',
        pretty_name: 'missing values fill',
        parameters: {},
        is_highlighted: false,
      },
      labelRemove: {
        name: 'labelRemove',
        pretty_name: 'labelRemove',
        parameters: {},
        is_highlighted: false,
      },
      oneHotEncode: {
        name: 'oneHotEncode',
        pretty_name: 'oneHotEncode',
        parameters: {},
        is_highlighted: false,
      },
    },
  },
  {
    name: 'agglomerativeClustering',
    pretty_name: 'agglomerativeClustering',
    parameters: {
      n_clusters: {
        name: 'n_clusters',
        pretty_name: 'n_clusters',
        value: 2,
        min: 1,
        max: 10,
        default: 2,
        description: '',
        is_highlighted: false,
        type: 'int',
      },
    },
    is_highlighted: false,
    models: {
      kmeans: {
        name: 'kmeans',
        pretty_name: 'kmeans clustering',
        parameters: {
          n_clusters: {
            name: 'n_clusters',
            pretty_name: 'number of clusters',
            value: 8,
            min: 1,
            max: 10,
            default: 8,
            description:
              'controls the number of groups that the algorithm is trying to find',
            is_highlighted: false,
            type: 'int',
          },
        },
        is_highlighted: false,
      },
      dbscan: {
        name: 'dbscan',
        pretty_name: 'density based clustering',
        parameters: {
          eps: {
            name: 'eps',
            pretty_name: 'epsilon',
            value: 0.1,
            min: 0,
            max: 1,
            default: 0.1,
            description: 'The maximum distance between two samples',
            is_highlighted: false,
            type: 'float',
          },
        },
        is_highlighted: false,
      },
      agglomerativeClustering: {
        name: 'agglomerativeClustering',
        pretty_name: 'agglomerativeClustering',
        parameters: {
          n_clusters: {
            name: 'n_clusters',
            pretty_name: 'n_clusters',
            value: 2,
            min: 1,
            max: 10,
            default: 2,
            description: '',
            is_highlighted: false,
            type: 'int',
          },
        },
        is_highlighted: false,
      },
    },
  },
  {
    name: 'pca2',
    pretty_name: 'pca2',
    parameters: {
      n_components: {
        name: 'n_components',
        pretty_name: 'n_components',
        value: 2,
        min: 0,
        max: 1,
        default: 2,
        description: '',
        is_highlighted: false,
        type: 'float',
      },
    },
    is_highlighted: false,
    models: {
      pca: {
        name: 'pca',
        pretty_name: 'pca',
        parameters: {
          n_components: {
            name: 'n_components',
            pretty_name: 'number of components',
            value: 2,
            min: 0,
            max: 1,
            default: 2,
            description:
              'The algorithm selects the number of components such that the amount of variance that needs to be explained is greater than the percentage specified by n_components',
            is_highlighted: false,
            type: 'float',
          },
        },
        is_highlighted: false,
      },
      pca2: {
        name: 'pca2',
        pretty_name: 'pca2',
        parameters: {
          n_components: {
            name: 'n_components',
            pretty_name: 'n_components',
            value: 2,
            min: 0,
            max: 1,
            default: 2,
            description: '',
            is_highlighted: false,
            type: 'float',
          },
        },
        is_highlighted: false,
      },
    },
  },
  {
    name: 'scatterplot',
    pretty_name: 'scatterplot',
    parameters: {},
    is_highlighted: false,
    models: {
      scatterplot: {
        name: 'scatterplot',
        pretty_name: 'scatterplot',
        parameters: {},
        is_highlighted: false,
      },
      clustermap: {
        name: 'clustermap',
        pretty_name: 'clustermap',
        parameters: {},
        is_highlighted: false,
      },
    },
  },
]
export { pipelineJson }
