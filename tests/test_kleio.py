from kleio import prov
from sc import provPopulator

a = prov

p = provPopulator.provPopulator()

a.ns("test", "http://tw.rpi.edu/ns/test#")

entity = a.Entity("test:entity")
entity.set_label("example entity")

activity = a.Activity("test:activity")
activity.set_label("example activity")

entity.set_was_generated_by(activity)
#print(a.serialize(format="turtle"))

p.addNameSpace('test3','https://test/for/purpose/')
a.clear_graph()
obj1 = p.createImageEntity("4f3ftge6wfew65fwc65ewfc65wfc65ew")
obj2 = p.createContainerActivity("67te76g33f2d7f32d52f3d326d532d")
p.addLabel(obj1,"haha")

print(a.serialize(format="turtle"))
print(p.serialize("turtle"))
