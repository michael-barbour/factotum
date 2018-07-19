from haystack.forms import FacetedSearchForm

class FacetedProductSearchForm(FacetedSearchForm):
  def __init__(self, *args, **kwargs):
    data = dict(kwargs.get("data", []))
    self.pucs = data.get('pucs', [])
    print('self.pucs %s' % data)
    self.brands = data.get('brand_name', [])
    self.models = data.get('facet_model_name',[])
    super(FacetedProductSearchForm, self).__init__(*args, **kwargs)

  def search(self):
    sqs = super(FacetedProductSearchForm, self).search()
    # The SearchQuerySet should only return Products and Data Documents
    sqs = sqs.filter(facet_model_name__in=['Data Document' ,'Product'])
    if self.pucs:
        query = None
        for puc in self.pucs:
            if query:
                query += u' OR '
            else:
                query = u''
            query += u'"%s"' % sqs.query.clean(puc)
        sqs = sqs.narrow(u'puc:%s' % query)
    if self.brands:
        query = None
        for brand in self.brands:
            if query:
                query += u' OR '
            else:
                query = u''
            query += u'"%s"' % sqs.query.clean(brand)
        sqs = sqs.narrow(u'brand_name_exact:%s' % query)
    if self.models:
        query = None
        for model in self.models:
            if query:
                query += u' OR '
            else:
                query = u''
            query += u'"%s"' % sqs.query.clean(model)
        sqs = sqs.narrow(u'facet_model_name:%s' % query)
    return sqs

class FacetedChemicalSearchForm(FacetedSearchForm):
    def __init__(self, *args, **kwargs):
      data = dict(kwargs.get("data", []))
      self.raw_chem_names = data.get('raw_chem_name', [])
      self.raw_cases = data.get('raw_cas',[])
      super(FacetedChemicalSearchForm, self).__init__(*args, **kwargs)

    def search(self):
      sqs = super(FacetedChemicalSearchForm, self).search()
      # The SearchQuerySet should only return Extracted Chemicals and DSSTox Substances
      sqs = sqs.filter(facet_model_name__in=['Extracted Chemical' ,'DSSTox Substance'])
      if self.raw_chem_names:
          query = None
          for raw_chem_name in self.raw_chem_names:
              if query:
                  query += u' OR '
              else:
                  query = u''
              query += u'"%s"' % sqs.query.clean(raw_chem_name)
          sqs = sqs.narrow(u'raw_chem_name_exact:%s' % query)
      if self.raw_cases:
          query = None
          for raw_cas in self.raw_cases:
              if query:
                  query += u' OR '
              else:
                  query = u''
              query += u'"%s"' % sqs.query.clean(raw_cas)
          sqs = sqs.narrow(u'raw_cas:%s' % query)
      return sqs